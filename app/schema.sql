BEGIN TRANSACTION;
PRAGMA foreign_keys=ON;

DROP TABLE IF EXISTS `LOGFILE_NAMES`;
DROP TABLE IF EXISTS `LOGS`;

CREATE TABLE `LOGFILE_NAMES` (
  `id` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
,  `file_name` varchar(128) NOT NULL 
);

CREATE TABLE `LOGS` (
  `id` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
, `logfile_name_id` integer NOT NULL 
, `date` varchar(128)
, `time` varchar(128) 
, `x-edge-location` varchar(128)
, `sc-bytes` integer 
, `c-ip` varchar(128)
, `cs-method` varchar(10)
, `cs(Host)` varchar(128)
, `cs-uri-stem` varchar(256)
, `sc-status` varchar(5)
, `cs(Referer)` varchar(256)
, `cs(User-Agent)` varchar(256)
, `cs-uri-query` varchar(256)
, `cs(Cookie)` varchar(256)
, `x-edge-result-type` varchar(10)
, `x-edge-request-id` varchar(256)
, `x-host-header` varchar(128)
, `cs-protocol` varchar(10)
, `cs-bytes` integer
, `time-taken` real 
, `x-forwarded-for` varchar(256)
, `ssl-protocol` varchar(256)
, `ssl-cipher` varchar(128)
, `x-edge-response-result-type` varchar(10)
, `cs-protocol-version` varchar(10)
, `fle-status` varchar(256)
, `fle-encrypted-fields` varchar(256)
, `c-port` integer
, `time-to-first-byte` real
, `x-edge-detailed-result-type` varchar(10)
, `sc-content-type` varchar(256)
, `sc-content-len` integer
, `sc-range-start` varchar(256)
, `sc-range-end` varchar(256)
,  CONSTRAINT `log_fk` FOREIGN KEY (`logfile_name_id`) REFERENCES `LOGFILE_NAMES` (`id`) ON DELETE CASCADE
);
DELETE FROM sqlite_sequence;
COMMIT;
