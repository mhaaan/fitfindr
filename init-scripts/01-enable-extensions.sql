-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
-- Enable PostGIS topology
CREATE EXTENSION IF NOT EXISTS postgis_topology;
-- Enable fuzzy string matching
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
-- Enable PostGIS tiger geocoder
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;