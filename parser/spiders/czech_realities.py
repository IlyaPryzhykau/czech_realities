"""
Spider for parsing categories, topics, questions, and answers from
cestina-pro-cizince.cz.
"""

import re
from datetime import datetime

import scrapy
from parser.items import (
    AnswerItem, CategoryItem, QuestionItem, TopicItem
)


class CzechRealitiesSpider(scrapy.Spider):
    """
    A spider that crawls 'cestina-pro-cizince.cz' and extracts:
    - Categories
    - Topics
    - Questions
    - Answers
    """

    name = 'czech_realities'
    allowed_domains = ['cestina-pro-cizince.cz']
    start_urls = [
        'https://cestina-pro-cizince.cz/obcanstvi/databanka-uloh/'
    ]

    def parse(self, response):
        """
        Parse the main page for category headers, yield CategoryItem,
        and then yield further Topics from each category.

        Args:
            response (scrapy.http.Response): The HTTP response from the start URL.

        Yields:
            CategoryItem: For each found category.
            TopicItem: Parsed from the subsequent 'h3' blocks.
            QuestionItem and AnswerItem: Recursively yielded from topics.
        """
        container = response.css('#vypisUloh')
        categories = container.css('h2.header_1, h2.header_2, h2.header_3')

        for category_sel in categories:
            category_name = category_sel.css('a::text').get()
            if category_name:
                category_name = category_name.strip()
                self.logger.debug(f"Found category: {category_name}")

                # Сохраняем категорию
                yield CategoryItem(name=category_name)

                # Парсим топики внутри категории
                yield from self.parse_topics(category_sel, category_name)

    def parse_topics(self, category_sel, category_name):
        """
        Parse topics under a given category selector.

        Args:
            category_sel (Selector): A scrapy selector pointing to <h2> or <h3> node for the category.
            category_name (str): The name of the category that these topics belong to.

        Yields:
            TopicItem: For each topic found in the siblings until the next category <h2>.
            QuestionItem and AnswerItem: Recursively yielded from these topics.
        """
        siblings = category_sel.xpath('./following-sibling::*')

        for sib in siblings:
            # Прерываем, когда нашли новую категорию (новый <h2>)
            if sib.root.tag == 'h2':
                break

            # Если это <h3> — внутри может быть топик
            if sib.root.tag == 'h3':
                topic_name = sib.css('a::text').get()
                if topic_name:
                    topic_name = topic_name.strip()
                    self.logger.debug(f"Found topic: {topic_name}")
                    yield TopicItem(
                        name=topic_name,
                        category_name=category_name
                    )

                # Следующий <ol> после <h3> содержит вопросы
                next_ol = sib.xpath('./following-sibling::*[1][self::ol]')
                if next_ol:
                    yield from self.parse_questions(next_ol[0], category_name, topic_name)

    def parse_questions(self, ol_sel, category_name, topic_name):
        """
        Parse question <li> blocks within an <ol>.

        Args:
            ol_sel (Selector): A scrapy selector pointing to the <ol> containing question <li>.
            category_name (str): Name of the parent category.
            topic_name (str): Name of the topic containing these questions.

        Yields:
            QuestionItem: Each question found.
            AnswerItem: Each answer to each question.
        """
        question_lis = ol_sel.css('li')
        for q_sel in question_lis:
            text_parts = q_sel.css('div.text ::text').getall()
            # Убираем лишние пробелы и объединяем текст
            raw_text = ' '.join(t.strip() for t in text_parts if t.strip())
            # Убираем лишние пробелы между словами и перед знаками препинания
            question_text = re.sub(r'\s+', ' ', raw_text)  # Заменяем любые последовательные пробелы на один
            question_text = re.sub(r'\s+([,.;?!])', r'\1', question_text)  # Убираем пробелы перед знаками препинания
            question_text = question_text.strip()

            # Иногда бывает <li> без "div.text" (вроде .spravnaOdpoved),
            # пропускаем их
            if not question_text:
                continue

            # Проверяем на наличие картинки
            image_url = q_sel.css('img::attr(src)').get()

            # Парсим дату обновления: "Datum aktualizace testové úlohy: 16. 12. 2024"
            update_text = q_sel.css('.datumAktualizace::text').get()
            update_date = None
            if update_text:
                match = re.search(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})', update_text)
                if match:
                    day, month, year = match.groups()
                    update_date = datetime(int(year), int(month), int(day)).date()

            # Генерируем QuestionItem
            self.logger.debug(f"Found question: {question_text[:50]}...")
            yield QuestionItem(
                text=question_text.strip(),
                image_url=image_url,
                update_date=update_date,
                topic_name=topic_name
            )

            # Генерируем ответы
            yield from self.parse_answers(q_sel, question_text)

    def parse_answers(self, q_sel, question_text):
        """
        Parse answers (both textual and image-based) to a given question.

        Args:
            q_sel (Selector): A scrapy selector pointing to the <li> that contains the question.
            question_text (str): The text of the question to which these answers belong.

        Yields:
            AnswerItem: For each possible answer (correct or incorrect).
        """
        all_answers = []

        img_wrappers = q_sel.css('div.imgAltWrapper')
        if img_wrappers:
            for wrapper in img_wrappers:
                onclick_value = wrapper.css('input::attr(onclick)').get() or ''
                is_correct = 'correct(1' in onclick_value
                image_url = wrapper.css('img::attr(src)').get()
                label_text = wrapper.css('label ::text').get(
                    default='').strip()

                all_answers.append({
                    'text': label_text,  # Будет 'A)', 'B)' и т.д.
                    'is_correct': is_correct,
                    'image_url': image_url
                })

        else:
            text_answers = q_sel.css(
                'ol.alternatives li:not(.spravnaOdpoved):not(.datumAktualizace):not(.citace)'
            )
            for wrapper in text_answers:
                onclick_value = wrapper.css('input::attr(onclick)').get() or ''
                is_correct = 'correct(1' in onclick_value
                label_text = ' '.join(
                    wrapper.css('label ::text').getall()).strip()
                raw_text = re.sub(r'\s+', ' ', label_text)
                answer_text = re.sub(r'\s+([,.;?!])', r'\1', raw_text)

                all_answers.append({
                    'text': answer_text,
                    'is_correct': is_correct,
                    'image_url': None
                })

        for ans in all_answers:
            self.logger.debug(
                f"Found answer: {ans['text']} (Image: {ans['image_url']})")
            yield AnswerItem(
                text=ans['text'],
                is_correct=ans['is_correct'],
                image_url=ans['image_url'],
                question_text=question_text
            )


