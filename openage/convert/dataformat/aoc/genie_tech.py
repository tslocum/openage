# Copyright 2019-2019 the openage authors. See copying.md for legal info.


from ...dataformat.converter_object import ConverterObject,\
    ConverterObjectGroup


class GenieTechObject(ConverterObject):
    """
    Technology in AoE2.

    Techs are not limited to researchable technologies. They also
    unlock the unique units of civs and contain the civ bonuses
    (excluding team boni).
    """

    def __init__(self, tech_id, full_data_set, members=None):
        """
        Creates a new Genie tech object.

        :param tech_id: The internal tech_id from the .dat file.
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        :param members: An already existing member dict.
        """

        super().__init__(tech_id, members=members)

        self.data = full_data_set
        self.data.genie_techs.update({self.get_id(): self})


class GenieTechEffectBundleGroup(ConverterObjectGroup):
    """
    A tech and the collection of its effects.
    """

    def __init__(self, tech_id, full_data_set):
        """
        Creates a new Genie tech group object.

        :param tech_id: The internal tech_id from the .dat file.
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        """

        super().__init__(tech_id)

        self.data = full_data_set
        self.data.tech_groups.update({self.get_id(): self})

        # The tech that belongs to the tech id
        self.tech = self.data.genie_techs[tech_id]

        # Effects of the tech
        effect_bundle_id = self.tech.get_member("tech_effect_id").get_value()

        if effect_bundle_id > -1:
            self.effects = self.data.genie_effect_bundles[effect_bundle_id]

        else:
            self.effects = None

    def is_researchable(self):
        """
        Techs are researchable if they have a valid research location.

        :returns: True if the research location id is greater than zero.
        """
        research_location_id = self.tech.get_member("research_location_id").get_value()

        # -1 = no train location
        if research_location_id == -1:
            return False

        return True

    def get_research_location(self):
        """
        Returns the group_id for a building line if the tech is
        researchable, otherwise return None.
        """
        if self.is_researchable():
            return self.tech.get_member("research_location_id").get_value()

        return None

    def has_effect(self):
        """
        Returns True if the techology's effects do anything.
        """
        if self.effects:
            return len(self.effects.get_effects()) > 0
        else:
            return False


class AgeUpgrade(GenieTechEffectBundleGroup):
    """
    Researches a new Age.

    openage actually does not care about Ages, so this will
    not be different from any other Tech API object. However,
    we will use this object to push all Age-related upgrades
    here and create a Tech from it.
    """

    def __init__(self, tech_id, age_id, full_data_set):
        """
        Creates a new Genie tech group object.

        :param tech_id: The internal tech_id from the .dat file.
        :param age_id: The index of the Age. (First Age = 0)
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        """

        super().__init__(tech_id, full_data_set)

        self.age_id = age_id

        self.data.age_upgrades.update({self.get_id(): self})


class UnitLineUpgrade(GenieTechEffectBundleGroup):
    """
    Upgrades a unit in a line.

    This will become a Tech API object targeted at the line's game entity.
    """

    def __init__(self, tech_id, unit_line_id, upgrade_target_id, full_data_set):
        """
        Creates a new Genie line upgrade object.

        :param tech_id: The internal tech_id from the .dat file.
        :param unit_line_id: The unit line that is upgraded.
        :param upgrade_target_id: The unit that is the result of the upgrade.
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        """

        super().__init__(tech_id, full_data_set)

        self.unit_line_id = unit_line_id
        self.upgrade_target_id = upgrade_target_id

        self.data.unit_upgrades.update({self.get_id(): self})


class BuildingLineUpgrade(GenieTechEffectBundleGroup):
    """
    Upgrades a building in a line.

    This will become a Tech API object targeted at the line's game entity.
    """

    def __init__(self, tech_id, building_line_id, upgrade_target_id, full_data_set):
        """
        Creates a new Genie line upgrade object.

        :param tech_id: The internal tech_id from the .dat file.
        :param building_line_id: The building line that is upgraded.
        :param upgrade_target_id: The unit that is the result of the upgrade.
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        """

        super().__init__(tech_id, full_data_set)

        self.building_line_id = building_line_id
        self.upgrade_target_id = upgrade_target_id

        self.data.building_upgrades.update({self.get_id(): self})


class UnitUnlock(GenieTechEffectBundleGroup):
    """
    Unlocks units and buildings for an Age, sometimes with additional
    requirements like (266 - Castle built).

    This will become one or more patches for an AgeUpgrade Tech. If the unlock
    is civ-specific, two patches (one for the age, one for the civ)
    will be created.
    """

    def __init__(self, tech_id, line_id, full_data_set):
        """
        Creates a new Genie tech group object.

        :param tech_id: The internal tech_id from the .dat file.
        :param line_id: The unit line that is unlocked.
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        """

        super().__init__(tech_id, full_data_set)

        self.line_id = line_id

        self.data.unit_unlocks.update({self.get_id(): self})


class CivBonus(GenieTechEffectBundleGroup):
    """
    Gives one specific civilization a bonus. Not the team bonus
    because that's not a Tech in Genie.

    This will become patches in the Civilization API object.
    """

    def __init__(self, tech_id, civ_id, full_data_set):
        """
        Creates a new Genie tech group object.

        :param tech_id: The internal tech_id from the .dat file.
        :param civ_id: The index of the civ.
        :param full_data_set: GenieObjectContainer instance that
                              contains all relevant data for the conversion
                              process.
        """

        super().__init__(tech_id, full_data_set)

        self.civ_id = civ_id

        self.data.civ_boni.update({self.get_id(): self})
