"""Checked data containers for what the model finds in a session."""

from pydantic import BaseModel, Field


class SessionItem(BaseModel):
    """One decision, open question, plan change or lesson from a session."""

    title: str = Field(min_length=1, description="A short title, at most ten words.")
    what: str = Field(min_length=1, description="What was decided, asked, changed or learned.")
    why: str = Field(description="The reason given in the session, or an empty string.")
    date: str = Field(description="The date it was said, as YYYY-MM-DD.")
    source_quote: str = Field(
        min_length=1,
        description="Exact words copied from the transcript that support the item.",
    )
    replaces: str = Field(
        description="The ID of an existing decision this replaces, such as D009, or 'none'.",
    )


class SessionExtraction(BaseModel):
    """Everything the model found in one session, sorted into four groups."""

    decisions: list[SessionItem]
    open_questions: list[SessionItem]
    changed_plans: list[SessionItem]
    lessons: list[SessionItem]
