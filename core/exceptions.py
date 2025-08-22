class SkillGapError(Exception):
    """Base exception for the app."""

class ParseError(SkillGapError):
    pass

class EmbeddingError(SkillGapError):
    pass

class CrawlError(SkillGapError):
    pass

class ConfigError(SkillGapError):
    pass
