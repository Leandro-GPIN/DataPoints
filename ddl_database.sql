-- Table: public.data_points

-- DROP TABLE public.data_points;

CREATE TABLE public.data_points
(
    latitude numeric(9,6),
    longitude numeric(9,6),
    rua character varying(100) COLLATE pg_catalog."default",
    bairro character varying(50) COLLATE pg_catalog."default",
    cidade character varying(50) COLLATE pg_catalog."default",
    estado character varying(50) COLLATE pg_catalog."default",
    pais character varying(50) COLLATE pg_catalog."default",
    numero character varying(50) COLLATE pg_catalog."default",
    cep character varying(50) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.data_points
    OWNER to postgres;
