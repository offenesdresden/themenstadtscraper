CREATE DATABASE themenstadtplan;
\c themenstadtplan
CREATE EXTENSION postgis;

CREATE TABLE elemente (
	properties json,
	location geometry	
);