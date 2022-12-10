create table doccano_speech2text(
    id BIGSERIAL PRIMARY KEY,
    annotation_id BIGINT,
    mongo_instance_id BIGINT,
    audio_filename VARCHAR(255),
    label TEXT,
    comment TEXT
);
-- # psql -h localhost -p 9000 --dbname=DC_Analytics -U hzh_dc_analytics
