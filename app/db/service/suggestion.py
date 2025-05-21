from app.db.models.concrete import Suggestion, SuggestionReaction
from datetime import datetime


def create_suggestion(title: str, text_content: str, date_posted: datetime, user_id: int, article_id: int):
    return (
        Suggestion(
            title=title,
            text_content=text_content,
            date_posted=date_posted,
            user_id=user_id,
            article_id=article_id
        ).save()
    )


def react_to_suggestion(suggestion_id: int, user_id: int, like: bool):
    return SuggestionReaction(suggestion_id=suggestion_id, user_id=user_id, like=like).save()


def get_suggestion_by_id(course_id: int):
    return Suggestion.get_by_id(course_id)


def get_suggestion_user_reaction(suggestion_id: int, user_id: int):
    return SuggestionReaction.get_reaction(suggestion_id, user_id)


def get_suggestion_reaction(suggestion_id: int):
    return SuggestionReaction.get_reactions_by_suggestion(suggestion_id)


def get_users_reactions(user_id: int):
    return SuggestionReaction.get_reactions_by_user(user_id)


def update_suggestion_by_id(course_id: int, **kwargs) -> int:
    return Suggestion.update_by_id(course_id, **kwargs)


def update_reaction_to_suggestion(suggestion_id: int, user_id: int, like: bool):
    return SuggestionReaction.update_reaction(suggestion_id, user_id, like)


def delete_suggestion_by_id(course_id: int) -> None:
    return Suggestion.delete_by_id(course_id)


def delete_suggestion_reaction(suggestion_id: int, user_id: int):
    return SuggestionReaction.delete_reaction(suggestion_id, user_id)
