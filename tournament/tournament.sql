-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.




create database tournament;
\c tournament
create table players(id serial primary key, name text); 
create table matches(match_id serial primary key, winner_id int, loser_id int);