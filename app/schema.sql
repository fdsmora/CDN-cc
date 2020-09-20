BEGIN TRANSACTION;
PRAGMA foreign_keys=ON;

DROP TABLE IF EXISTS Logfiles;

CREATE TABLE `Logfiles` (
  `id` integer  NOT NULL PRIMARY KEY AUTOINCREMENT
,  `file_name` varchar(128) NOT NULL 
);

--DELETE FROM sqlite_sequence;
--CREATE INDEX "idx_custom_attributes_contact_id" ON "custom_attributes" (`contact_id`);
--CREATE INDEX "idx_contacts_team_id" ON "contacts" (`team_id`);
COMMIT;
