-- create database stocks_crawler
DROP DATABASE IF EXISTS stocks_crawler;
CREATE DATABASE IF NOT EXISTS stocks_crawler;

USE stocks_crawler;

-- create markets
CREATE TABLE IF NOT EXISTS markets (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  market_name VARCHAR(5) NOT NULL UNIQUE,
  description VARCHAR(50) DEFAULT ''
);

-- create sectors
CREATE TABLE IF NOT EXISTS sectors (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  parent INT DEFAULT NULL,
  sector_name VARCHAR(50) NOT NULL UNIQUE,
  CONSTRAINT fk_parent_sectors FOREIGN KEY (parent) REFERENCES sectors(id)
);

-- create industries
CREATE TABLE IF NOT EXISTS industries (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  parent INT DEFAULT NULL,
  sector_id INT NOT NULL,
  industry_name VARCHAR(50) NOT NULL UNIQUE,
  CONSTRAINT fk_parent_industries FOREIGN KEY (parent) REFERENCES industries(id),
  CONSTRAINT fk_industries_sector FOREIGN KEY (sector_id) REFERENCES sectors(id)
);

-- create stocks
CREATE TABLE IF NOT EXISTS stocks (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  market_id INT NOT NULL,
  industry_id INT NOT NULL,
  stock_code VARCHAR(4) NOT NULL,
  description VARCHAR(50) DEFAULT '',
  is_active TINYINT NOT NULL DEFAULT 1,
  CONSTRAINT fk_stocks_market FOREIGN KEY (market_id) REFERENCES markets(id),
  CONSTRAINT fk_stocks_industry FOREIGN KEY (industry_id) REFERENCES industries(id)
);

-- create histories
CREATE TABLE IF NOT EXISTS histories (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  stock_id INT NOT NULL,
  history_date DATE NOT NULL,
  open DECIMAL(10,4) NOT NULL,
  high DECIMAL(10,4) NOT NULL,
  low DECIMAL(10,4) NOT NULL,
  close DECIMAL(10,4) NOT NULL,
  volume INT NOT NULL,
  dividend DECIMAL(9,4) DEFAULT 0.0,
  split DECIMAL(5,2) DEFAULT 0.0,
  CONSTRAINT fk_histories_stock FOREIGN KEY(stock_id) REFERENCES stocks(id)
);
