-- Minimal seed data for cards and example price snapshots
INSERT INTO cards (id, category, set_name, year, title, number, variant) VALUES
(1, 'Pokemon', 'Base Set', '1999', 'Charizard Holo #4', '4', 'Holo'),
(2, 'NBA', 'Prizm', '2019', 'Ja Morant #249 Base', '249', 'Base'),
(3, 'Pokemon', 'Base Set', '1999', 'Blastoise Holo #2', '2', 'Holo')
ON CONFLICT DO NOTHING;
