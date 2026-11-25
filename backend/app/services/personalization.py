
from app.models.user_profile import UserProfile


def build_personalization_context(
    profile: UserProfile | None,
) -> str:
    """
    Build AI instructions using the musician's saved preferences.
    """

    if profile is None:
        return ""

    context = [
        "PERSONALIZED MUSICIAN CONTEXT",
        "",
        "Adapt your responses using the following profile.",
        "Treat these details as preferences, not verified expertise.",
    ]

    context.append(
        f"Experience level: {profile.experience_level}"
    )

    context.append(
        f"Preferred learning level: "
        f"{profile.preferred_learning_level}"
    )

    if profile.musical_background:
        context.append(
            f"Musical background: {profile.musical_background}"
        )

    if profile.primary_instrument:
        context.append(
            f"Primary instrument: {profile.primary_instrument}"
        )

    if profile.years_of_experience is not None:
        context.append(
            f"Years of experience: {profile.years_of_experience}"
        )

    if profile.favorite_ragas:
        context.append(
            "Favorite ragas: "
            + ", ".join(profile.favorite_ragas)
        )

    if profile.musical_goals:
        context.append(
            "Musical goals: "
            + ", ".join(profile.musical_goals)
        )

    context.extend([
        "",
        "PERSONALIZATION GUIDELINES",
        "- Match explanation complexity to the preferred learning level.",
        "- Use the primary instrument for relevant practice examples.",
        "- Use favorite ragas as examples when relevant to the question.",
        "- Connect suggestions to the musician's stated goals.",
        "- Explain unfamiliar technical terminology appropriately.",
        "- Do not force personal preferences into unrelated answers.",
        "- Never assume skills or achievements not stated in the profile.",
        "- Always prioritize factual Carnatic music accuracy.",
    ])

    return "\n".join(context)
