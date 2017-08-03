"""test resultdb"""
from result import ResultDB
from player import PlayerDB

playerdb = PlayerDB('data/pellaajat')
result = ResultDB('data/results.htm', playerdb)
