# TODO: Write subclass of Adventurer to represent non-wildcard enemies.
class Adventurer():
    """This is supposed to represent a multi-line comment.

        More words.
        Even more wordy words.
        words galore.
    """
    def __init__(
        self,
        hindrances=None,
        edges=None,
        powers=None,

        agility=4,
        # agility-linked skills
        athletics=4,
        stealth=4,

        smarts=4,
        # smarts skills
        common_knowledge=4,
        notice=4,
        academics=0,
        battle=0,

        spirit=4,
        # spirit skills
        persuasion=4,

        strength=4,
        # strength skills

        vigor=4
        # vigor skills
    ):
        # BUG: this is a bug
        self.hindrances = hindrances
        self.edges = edges
        self.powers = powers
        self.agility = agility
        self.smarts = smarts
        self.spirit = spirit
        self.strength = strength
        self.vigor = vigor
        self.athletics = athletics
        self.common_knowledge = common_knowledge
        self.notice = notice
        self.persuasion = persuasion
        self.stealth = stealth

        # hindrances, edges, and powers will be set by passing in lists.

        # TODO: write methods to calculate compound attributes.

        # first comment
        # second comment
        # FIXME: problem, officer?
        # fourth comment
        # fiff



