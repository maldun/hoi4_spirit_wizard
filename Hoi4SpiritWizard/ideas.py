#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import shutil
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
    INDENT = 1*" "
    YML_SUFF = ".yml"
    GFX_SUFF = ".gfx"
    TXT_SUFF = ".txt"
    
    def __init__(self, name):
        self.name = name

    def create_gfx_object(self, fname, picture_name=None):
        """
        Takes a relative file name fname and creates the necessary
        gfx code
        """

        gfx_name = self.GFX_PREFIX + (self.name if picture_name is None else picture_name)
        inner_list = [[self.NAME_KEY, [gfx_name]],[self.TEXTURE_FILE_KEY, [fname]]]
        outer_list = [[self.SPRITE_TYPE, inner_list]]
        return outer_list

    def create_localisation(self, full_name, description, lang = "english"):
        """
        Writes out the localisation text
        """
        text = f"l_{lang}:\n"
        text += self.INDENT + self.name + f':0 "{full_name}"\n'
        text += self.INDENT + self.name + f'_desc:0 "{description}"'
        return text
        
    def write_obj(self, obj):
        """
        Writes a paradox object
        """
        return list2paradox(obj)

    @staticmethod
    def write_file(outfile, code, path=''):
        if path != '':
            outfile = os.path.join(path, outfile)
        with open(outfile, 'w') as fp:
            fp.write(code)
    
    def _write_gfx_file(self, fname, picture_name=None, path=''):
        """
        Takes the input and writes the GFX_file
        """
        obj = self.create_gfx_object(fname, picture_name)
        outer_obj = [[self.SPRITE_TYPES, obj]]
        code = self.write_obj(outer_obj)
        outfile = self.name + self.GFX_SUFF
        self.write_file(outfile, code, path=path)
        return code

    def _write_localisation_file(self, full_name, description, lang='english', path=''):
        code = self.create_localisation(full_name, description, lang=lang)
        outfile = self.name + self.YML_SUFF
        self.write_file(outfile, code, path=path)
        return code

    
        
########################
# Tests                #
########################

class IdeaTests(unittest.TestCase):
    GFX_FILE = "gfx/interface/ideas/filename.dds"
    def setUp(self):
        self.idea = Idea('my_idea_1')
        
    def test_create_gfx_object(self):
        obj = self.idea.create_gfx_object(self.GFX_FILE)
        expected_code = """
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }"""
        expected_obj = code2list(expected_code)
        self.assertEqual(expected_obj, obj)

    def test_write_obj(self):
        obj = self.idea.create_gfx_object(self.GFX_FILE)
        expected_code = """
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }"""
        expected_obj = code2list(expected_code)
        expected_code = list2paradox(expected_obj)
        resulting_code = list2paradox(obj)
        self.assertEqual(expected_code, resulting_code)

    def test_create_localisation(self):
        name = "Idea's Name"
        desc = "Idea's Desription"
        result = self.idea.create_localisation(name, desc).splitlines()
        self.assertEqual(result[0].strip(), "l_english:")
        self.assertIn(self.idea.INDENT + f'{self.idea.name}:0', result[1])
        self.assertIn(self.idea.INDENT + f'{self.idea.name}_desc:0', result[2])

    def test__write_gfx_file(self):
        code = self.idea._write_gfx_file(self.GFX_FILE)
        fname = self.idea.name + self.idea.GFX_SUFF
        self.assertTrue(os.path.isfile(fname))
        os.remove(fname)
        
        expected_code = """spriteTypes = {
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }}"""
        expected_obj = code2list(expected_code)
        expected_code = list2paradox(expected_obj)
        self.assertEqual(code, expected_code)

    def test__write_localisation_file(self):
        name = "Idea's Name"
        desc = "Idea's Desription"
        result = self.idea._write_localisation_file(name, desc).splitlines()
        fname = self.idea.name + self.idea.YML_SUFF
        self.assertTrue(os.path.isfile(fname))
        os.remove(fname)
        self.assertEqual(result[0].strip(), "l_english:")
        self.assertIn(self.idea.INDENT + f'{self.idea.name}:0', result[1])
        self.assertIn(self.idea.INDENT + f'{self.idea.name}_desc:0', result[2])
