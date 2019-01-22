#!/usr/bin/env python
# encoding: utf-8

"""
@author: lvguangchao
@email: guangchao.lv@qq.com
@file: ExcelImportManager.py
@time: 2017/11/28 11:42
"""
__playlog = dict()
__playlogAuto = dict()
__playlogExport = dict()
__PlatDataSyn = dict()
__CheckAccount = dict()


def getplaylogDict():
    return __playlog


def getplaylogAutoDict():
    return __playlogAuto


def getplaylogExport():
    return __playlogExport


def getPlatDataSyn():
    return __PlatDataSyn


def getCheckAccount():
    return __CheckAccount
