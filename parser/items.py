import scrapy


class CategoryItem(scrapy.Item):
    """
    Represents a category in the database.

    Attributes:
        name (str): The name of the category.
    """
    name = scrapy.Field()


class TopicItem(scrapy.Item):
    """
    Represents a topic within a category.

    Attributes:
        name (str): The name of the topic.
        category_name (str): The name of the parent category to which
            this topic belongs.
    """
    name = scrapy.Field()
    category_name = scrapy.Field()


class QuestionItem(scrapy.Item):
    """
    Represents a question within a topic.

    Attributes:
        text (str): The text of the question.
        image_url (str | None): An optional URL for an image associated
            with the question.
        update_date (str): The last update date of the question
            in 'dd.mm.yyyy' format.
        topic_name (str): The name of the topic to which this question belongs.
    """
    text = scrapy.Field()
    image_url = scrapy.Field()
    update_date = scrapy.Field()
    topic_name = scrapy.Field()


class AnswerItem(scrapy.Item):
    """
    Represents an answer to a question.

    Attributes:
        text (str): The text of the answer.
        image_url (str | None): An optional URL for an image associated
            with the answer.
        is_correct (bool): Indicates whether the answer is correct.
        question_text (str): The text of the question to which this
            answer belongs.
    """
    text = scrapy.Field()
    image_url = scrapy.Field()
    is_correct = scrapy.Field()
    question_text = scrapy.Field()
