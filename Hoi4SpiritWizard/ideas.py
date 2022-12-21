#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
import shutil
from Hoi4Converter.converter import list2paradox
from Hoi4Converter.parser import parse_grammar as code2list

class Modifier:
    """
    This class represents modifiers.
    """
    MISSING_ERROR_MSG = "Error: Field {} missing!"
    FIELDS = ["Key", "Value"]
    NAME = "modifier"
    def __init__(self, entries):
        self.keys = {}
        self.entries = entries
        self.set_fields(**entries)
        
    def set_keys(self):
        new_keys = {"political_power_cost",
                    "stability_factor"}
        self.keys.update(new_keys)

    def to_pdx(self):
        """
        Key method to adapt
        """
        key = getattr(self, self.FIELDS[0])
        val = getattr(self, self.FIELDS[1])
        return [key, [val]]
    
    @classmethod
    def get_name(cls):
        return cls.NAME
    
    @classmethod
    def get_fields(cls):
        return cls.FIELDS

    def set_fields(self, **kwargs):
        for key in self.FIELDS:
            if key in kwargs.keys():
                setattr(self, key, kwargs[key])
            else:
                raise Exception(self.MISSING_ERROR_MSG.format(key))

class ResearchBonus(Modifier):
    NAME = "research_bonus"

class TargetedModifier(Modifier):
    NAME = "targeted_modifier"
        
class Idea:
    """
    A class which represents an HOI4 idea 
    and is turned into code
    """
    GFX_PREFIX = "GFX_idea_"
    IDEAS_KEY = 'ideas'
    COUNTRY_KEY = 'country'
    TEXTURE_FILE_KEY = "texturefile"
    SPRITE_TYPE = "spriteType"
    SPRITE_TYPES = "spriteTypes"
    INDENT = 1*" "
    LOC_SUFF = ".yml"
    GFX_SUFF = ".gfx"
    PDX_SUFF = ".txt"

    NAME_KEY = "name"
    
    GFX_FNAME = "GFXFileName"
    PIC_NAME = "PictureName"
    FULL_NAME = "FullName"
    DESC = "Description"

    MISSING_ERROR_MSG = "Error: {} missing!"

    KEYS = [GFX_FNAME, PIC_NAME, FULL_NAME, DESC]

    # Categories of options
    MODIFIER = "modifier"
    TARGETED_MODIFIER = "targeted_modifier"

    CATEGORIES = [Modifier, ResearchBonus]
    
    def __init__(self, name):
        self.name = name
        self.category_objs = {}

    def create_gfx_object(self, fname, picture_name=None):
        """
        Takes a relative file name fname and creates the necessary
        gfx code
        """

        gfx_name = self.GFX_PREFIX + (self.name if picture_name is None else picture_name)
        inner_list = [[self.NAME_KEY, [gfx_name]],[self.TEXTURE_FILE_KEY, [fname]]]
        outer_list = [[self.SPRITE_TYPE, inner_list]]
        return outer_list

    def create_localisation(self, full_name, description):
        """
        Writes out the localisation text
        """
        text = ''
        text += self.INDENT + self.name + f':0 "{full_name}"\n'
        text += self.INDENT + self.name + f'_desc:0 "{description}"'
        return text

    def write_localisation(self):
        if hasattr(self, self.FULL_NAME):
            fname = getattr(self, self.FULL_NAME)
        else:
            raise AttributeError(self.MISSING_ERROR_MSG.format(self.FULL_NAME))
        if hasattr(self, self.DESC):
            description = getattr(self, self.DESC)
        else:
            raise AttributeError(self.MISSING_ERROR_MSG.format(self.DESC))
        return self.create_localisation(fname, description)
        
    def write_obj(self, obj):
        """
        Writes a paradox object
        """
        return list2paradox(obj)

    def _write_gfx_obj(self, fname, picture_name=None):
        """
        Takes the input and writes the GFX_file
        """
        obj = self.create_gfx_object(fname, picture_name)
        return obj

    def write_gfx_obj(self):
        if hasattr(self, self.GFX_FNAME):
            fname = getattr(self, self.GFX_FNAME)
        else:
            raise AttributeError(f"Error: {self.GFX_FNAME} missing!")
        if hasattr(self, self.PIC_NAME):
            picture_name = getattr(self, self.PIC_NAME)
        else:
            picture_name = None
        return self._write_gfx_obj(fname,picture_name=picture_name) 
        
    
    def set_dict(self, dic):
        for key, val in dic.items():
            setattr(self, key, val)

    def set_category_objs(self, category_cls, cobjs):
        cat_name = category_cls.get_name()
        self.category_objs[cat_name] = cobjs
            
    def write_idea_paradox(self):
        idea_val = []
        for cat in self.CATEGORIES:
            cat_name = cat.get_name()
            cobjs = self.category_objs[cat_name]
            cpdx = [cobj.to_pdx() for cobj in cobjs]
            idea_val += [[cat_name, cpdx]]
            
        idea_obj = [self.name, idea_val]
        return idea_obj
    
    def write_idea(self, path=''):
        self.write_gfx_file(path=path)

    @staticmethod
    def write_file(code, outfile, path=''):
        if path != '':
            outfile = os.path.join(path, outfile)
        with open(outfile, 'w') as fp:
            fp.write(code)
    
    @classmethod
    def write_gfx_file(cls,idea_list, outfile, path=''):
        obj_list = []
        for idea in idea_list:
            obj_list += idea.write_gfx_obj() 
        outer_obj = [[cls.SPRITE_TYPES, obj_list]]
        code = list2paradox(outer_obj)
        cls.write_file(code, outfile, path=path)
        return outer_obj

    @classmethod
    def write_localisation_file(cls, idea_list, outfile, path='', lang='english'):
        text = f"l_{lang}:\n"
        for idea in idea_list:
            text += idea.write_localisation()
        cls.write_file(text, outfile, path=path)
        return text

    @classmethod
    def write_paradox_file(cls, idea_list, outfile, path=''):
        idea_obj = []
        for idea in idea_list:
            idea_obj += idea.write_idea_paradox()
        paradox_obj = [[cls.IDEAS_KEY, [[cls.COUNTRY_KEY, [idea_obj]]]]]
        code = list2paradox(paradox_obj)
        cls.write_file(code, outfile, path=path)
        return paradox_obj
        
########################
# Tests                #
########################

class IdeaTests(unittest.TestCase):
    GFX_FILE = "gfx/interface/ideas/filename.dds"
    def setUp(self):
        self.idea = Idea('my_idea_1')
        self.GFX_data = {self.idea.GFX_FNAME: "gfx/interface/ideas/filename.dds"}
        self.loc_data = {Idea.FULL_NAME: "Idea's Name", Idea.DESC: "Idea's Desription"}
        
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
        #self.assertEqual(result[0].strip(), "l_english:")
        self.assertIn(self.idea.INDENT + f'{self.idea.name}:0', result[0])
        self.assertIn(self.idea.INDENT + f'{self.idea.name}_desc:0', result[1])

    def test_write_localisation_file(self):
        self.idea.set_dict(self.loc_data)
        out_file = self.idea.name + Idea.LOC_SUFF

        result = Idea.write_localisation_file([self.idea],out_file).splitlines()
        self.assertTrue(os.path.isfile(out_file))
        os.remove(out_file)

        self.assertEqual(result[0].strip(), "l_english:")
        self.assertIn(self.idea.INDENT + f'{self.idea.name}:0', result[1])
        self.assertIn(self.idea.INDENT + f'{self.idea.name}_desc:0', result[2])

    def test__write_gfx_obj(self):
        obj = self.idea._write_gfx_obj(self.GFX_FILE)
        expected_code = """
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }"""
        expected_obj = code2list(expected_code)
        self.assertEqual(obj, expected_obj)

    def test_write_gfx_obj(self):
        self.idea.set_dict(self.GFX_data)
        obj = self.idea.write_gfx_obj()
        expected_code = """
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }"""
        expected_obj = code2list(expected_code)
        self.assertEqual(obj, expected_obj)

    def test_write_gfx_file(self):
        fname = self.idea.name + self.idea.GFX_SUFF
        self.idea.set_dict(self.GFX_data)
        obj = Idea.write_gfx_file([self.idea], fname)
        expected_code = """spriteTypes = {
        spriteType = {
            name = GFX_idea_my_idea_1
            texturefile = gfx/interface/ideas/filename.dds
            }}"""
        expected_obj = code2list(expected_code)
        self.assertEqual(obj, expected_obj)
        self.assertTrue(os.path.isfile(fname))
        os.remove(fname)

    def test_write_paradox_file(self):
        fname = self.idea.name + self.idea.PDX_SUFF
        obj = Idea.write_paradox_file([self.idea], fname)
        
        expected_code = """ideas = {
        country = {
            my_idea_1 ={}
            }}"""
        expected_obj = code2list(expected_code)

        self.assertEqual(obj, expected_obj)
        self.assertTrue(os.path.isfile(fname))
        os.remove(fname)


