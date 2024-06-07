USE textgen;
CREATE TABLE IF NOT EXISTS generated_text (
    id UUID PRIMARY KEY,
    prompt text,
    texts text
);