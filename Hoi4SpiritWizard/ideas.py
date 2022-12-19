#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from Hoi4Converter.converter import list2paradox
from Hoi4Converter.parser import parse_grammar as code2list

class Idea:
    """
    A class which represents an HOI4 idea 
    and is turned into code
    """
    GFX_PREFIX = "GFX_idea_"
    NAME_KEY = "name"
    TEXTURE_FILE_KEY = "texturefile"
    SPRITE_TYPE = "spriteType"
    SPRITE_TYPES = "spriteTypes"

    def __init__(self, name):
        self.name = name

    def set_gfx_object(self, fname, picture_name=None):
        """
        Takes a relative file name fname and creates the necessary
        gfx code
        """

        gfx_name = self.GFX_PREFIX + (self.name if picture_name is None else picture_name)
        inner_list = [[self.NAME_KEY, [gfx_name]],[self.TEXTURE_FILE_KEY, [fname]]]
        outer_list = [[self.SPRITE_TYPE, inner_list]]
        return outer_list

    def write_obj(self, obj):
        """
        Writes a paradox object
        """
        return list2paradox(obj)

    

    
        
########################
# Tests                #
########################

class IdeaTests(unittest.TestCase):
    GFX_FILE = "gfx/interface/ideas/filename.dds"
    def setUp(self):
        self.idea = Idea('my_idea_1')
        
    def test_set_gfx_object(self):
        obj = self.idea.set_gfx_object(self.GFX_FILE)
        expected_code = """
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }"""
        expected_obj = code2list(expected_code)
        self.assertEqual(expected_obj, obj)

    def test_write_obj(self):
        obj = self.idea.set_gfx_object(self.GFX_FILE)
        expected_code = """
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }"""
        expected_obj = code2list(expected_code)
        expected_code = list2paradox(expected_obj)
        resulting_code = list2paradox(obj)
        self.assertEqual(expected_code, resulting_code)
        
    
