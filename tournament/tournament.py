#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2,bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
	"""Remove all the match records from the database."""
	conn = connect()
	c = conn.cursor()
	c.execute("delete from matches;")
	conn.commit() 
	conn.close()


def deletePlayers():
    
	"""Remove all the player records from the database."""
	conn = connect()
	c = conn.cursor()
	c.execute("delete from players;")
	conn.commit() 
	conn.close()



def countPlayers():
    
	"""Returns the number of players currently registered."""
	conn = connect()
	c = conn.cursor()
	c.execute("select count(*) from players")
	counts=c.fetchall()
	conn.close()
	return counts[0][0]


def registerPlayer(name):

	
	conn = connect()
	c = conn.cursor()
	c.execute("insert into players(name) values(%s)",(bleach.clean(name),))
	conn.commit() 
	conn.close()

def playerStandings():

	conn = connect()
	c = conn.cursor()
	c.execute("select p.id,p.name,"
	"sum(case when m.winner_id=p.id then 1 else 0 end)as wins, "
	"count(m.*) "
	"from players as p left join matches as m "
	"on p.id=m.winner_id or p.id=m.loser_id "
	"group by p.id order by wins desc;")
	
	list=c.fetchall()
	conn.close()
	return list

def reportMatch(winner, loser):
	conn = connect()
	c = conn.cursor()
	c.execute("insert into matches(winner_id,loser_id) values((%s),(%s))",(winner,loser))
	conn.commit() 
	conn.close()
	return 


def swissPairings():
	conn = connect()
	c = conn.cursor()
	c.execute("select p.id,p.name,"
	"count(p.id) as wins "
	"from players as p left join matches as m "
	"on p.id=m.winner_id "
	"group by p.id order by wins desc;")
	result=c.fetchall()
	l=[]
	i=0
	while len(result) >0:
		l.append((result[0][0], result[0][1],result[1][0], result[1][1]))
		result.pop(0)
		result.pop(0)
		
	conn.close()
	return l

