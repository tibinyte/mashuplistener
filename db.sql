CREATE TABLE watches (
    id SERIAL PRIMARY KEY,
    serverid bigint,
    name TEXT,
    channelid bigint,
    gymlink TEXT
);

CREATE TABLE processed (
    submissionid bigint,
    watchid bigint
);
