BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "celestial_body" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	"type"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "astronaut" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	"specialization"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "alien_encounter" (
	"id"	INTEGER NOT NULL,
	"description"	VARCHAR(100) NOT NULL,
	"location"	VARCHAR(50) NOT NULL,
	"date"	VARCHAR(20) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "mission_details" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	"destination"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "spacecraft" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	"launch_date"	VARCHAR(20) NOT NULL,
	"mission_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("mission_id") REFERENCES "mission_details"("id")
);
CREATE TABLE IF NOT EXISTS "experiment" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50) NOT NULL,
	"results"	VARCHAR(100) NOT NULL,
	"spacecraft_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("spacecraft_id") REFERENCES "spacecraft"("id")
);
INSERT INTO "celestial_body" VALUES (1,'Earth','Planet334467');
INSERT INTO "celestial_body" VALUES (3,'Mars','Planet');
INSERT INTO "celestial_body" VALUES (4,'Venus','Planet2');
INSERT INTO "celestial_body" VALUES (5,'Ayush','Planet1');
INSERT INTO "astronaut" VALUES (1,'Neil Armstrong','Commander');
INSERT INTO "astronaut" VALUES (2,'Curiosity Rover','Rover');
INSERT INTO "astronaut" VALUES (3,'Carl Sagan','Astrophysicist');
INSERT INTO "alien_encounter" VALUES (1,'Unknown flying object','Space','2023-01-15');
INSERT INTO "alien_encounter" VALUES (2,'Strange signal','Proxima Centauri','2024-05-20');
INSERT INTO "alien_encounter" VALUES (3,'Unexplained phenomenon','Orion Nebula','2022-11-08');
INSERT INTO "mission_details" VALUES (1,'Apollo 11 Moon Landing','Moon');
INSERT INTO "mission_details" VALUES (2,'Voyager Interstellar Mission','Outer Space');
INSERT INTO "mission_details" VALUES (3,'Curiosity Mars Exploration','Mars');
INSERT INTO "spacecraft" VALUES (1,'Apollo 11','1969-07-16',1);
INSERT INTO "spacecraft" VALUES (2,'Curiosity','2011-11-26',3);
INSERT INTO "spacecraft" VALUES (3,'Voyager 1','1977-09-05',2);
INSERT INTO "experiment" VALUES (1,'Microgravity Study','Zero-G achieved',1);
INSERT INTO "experiment" VALUES (2,'Mars Soil Analysis','Water presence detected',3);
INSERT INTO "experiment" VALUES (3,'Voyager Imaging','Captured images of outer planets',2);
COMMIT;
