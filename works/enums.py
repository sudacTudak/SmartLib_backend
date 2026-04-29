from common_core.enums import AppStrEnum

__all__ = ["WorkCategory"]


class WorkCategory(AppStrEnum):
    Book = "book"
    ScientificArticle = "scientific_article"
    CollectedArticles = "collected_articles"
    Journal = "journal"
    Comic = "comic"
    LectureNotes = "lecture_notes"

