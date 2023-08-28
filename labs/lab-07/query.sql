SELECT name FROM  songs;
SELECT name FROM songs ORDER BY tempo;
SELECT name FROM songs ORDER BY duration_ms DESC LIMIT 5;
SELECT name FROM songs WHERE danceability > 0.75 AND energy > 0.75 AND valence > 0.75;
SELECT AVG(energy) AS average_energy FROM songs;
SELECT name FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Post Malone');
SELECT AVG(energy) FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Drake');
SELECT name FROM songs WHERE name LIKE "%feat.%";

-- Answers:
-- 1) According to the average numbers on energy (0.65906), danceability (0.71646) and valence (0.484443 ),
-- it seems that the 2018 listeners' aura was Blue (wistful or emotional, and this hue reflects listeners
-- who seek out music to feel their feelings out loud).

-- 2) The way I calculated it may not be the most representative because they are only the 100 most listened to
-- in the world, there are a lot more songs. Besides that some users may not like these songs or
-- even listen to them. So it's better to give, like
-- Spotify does, an analysis of each user's Aura for themselves.
-- Finally, another problem is personal interpretation.
-- The fact that a song has low valence, energy, and danceability
-- doesn't necessarily indicate that the listener isn't uplifted by it.
