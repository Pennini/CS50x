-- Keep a log of any SQL queries you execute as you solve the mystery.


-- Answer:
-- The THIEF is: Bruce
-- The city the thief ESCAPED TO: New York City
-- The ACCOMPLICE is: Robin


-- Query to see the description of the crime and value information to continue the case
SELECT description FROM crime_scene_reports WHERE day = 28 AND month = 7 AND street = 'Humphrey Street';

-- Get the transcript of the people who was interviewed and see where to start the investigation
SELECT name, transcript
FROM interviews
WHERE month = 7
   AND day = 28;

-- See the activity and the license plate from who left the bakery at the time frame that Ruth said in the interview
SELECT activity, license_plate
FROM bakery_security_logs
WHERE month = 7
   AND day = 28
   AND hour = 10
   AND minute > 14
   AND minute < 26;

-- Investigate who withdrew some money at the Leggett Street like Eugene ponctuated
SELECT name
FROM bank_accounts ba
JOIN people p ON ba.person_id = p.id
WHERE ba.account_number IN (
   SELECT account_number
   FROM atm_transactions
   WHERE month = 7
      AND day = 28
      AND atm_location = "Leggett Street"
      AND transaction_type = "withdraw"
);

-- See who was talking at the phone that day for less than a minute with the help of Raymond information
SELECT name
FROM people p
WHERE phone_number IN (
      SELECT caller
      FROM phone_calls
      WHERE day = 28
      AND month = 7
      AND duration < 61
   )
   OR phone_number IN (
      SELECT receiver
      FROM phone_calls
      WHERE day = 28
      AND month = 7
      AND duration < 61
   );

-- See the earliest flight for the next day
SELECT id, hour, minute
FROM flights
WHERE month = 7
   AND day = 29
   ORDER BY hour, minute
   LIMIT 1;

-- See the people that was in the earliest flight of the day 29 like Raymond told me to do
SELECT name
FROM people p
JOIN passengers pg ON p.passport_number = pg.passport_number
WHERE flight_id IN (
   SELECT id
   FROM flights
   WHERE month = 7
      AND day = 29
      ORDER BY hour, minute
      LIMIT 1
);

-- See who is the thief Using the information seen before
SELECT name
FROM people p
JOIN bank_accounts ba ON ba.person_id = p.id
JOIN passengers pg ON p.passport_number = pg.passport_number
WHERE p.phone_number IN (
      SELECT caller
      FROM phone_calls
      WHERE day = 28
      AND month = 7
      AND duration < 60
   )
   AND pg.flight_id IN (
      SELECT id
      FROM flights
      WHERE month = 7
         AND day = 29
         ORDER BY hour, minute
         LIMIT 1
   )
   AND ba.account_number IN (
      SELECT account_number
      FROM atm_transactions
      WHERE month = 7
         AND day = 28
         AND atm_location = "Leggett Street"
         AND transaction_type = "withdraw"
   )
   AND p.license_plate IN (
      SELECT license_plate
      FROM bakery_security_logs
      WHERE month = 7
         AND day = 28
         AND hour = 10
         AND minute > 14
         AND minute < 26
   );
-- See who is the accomplice by seeing who the thief was talking to that day
SELECT name
FROM people p
JOIN phone_calls ph ON p.phone_number = ph.receiver
WHERE ph.caller IN (
      SELECT phone_number
      FROM people p
      JOIN bank_accounts ba ON ba.person_id = p.id
      JOIN passengers pg ON p.passport_number = pg.passport_number
      WHERE p.phone_number IN (
      SELECT caller
      FROM phone_calls
      WHERE day = 28
      AND month = 7
      AND duration < 60
   )
   AND pg.flight_id IN (
      SELECT id
      FROM flights
      WHERE month = 7
         AND day = 29
         ORDER BY hour, minute
         LIMIT 1
   )
   AND ba.account_number IN (
      SELECT account_number
      FROM atm_transactions
      WHERE month = 7
         AND day = 28
         AND atm_location = "Leggett Street"
         AND transaction_type = "withdraw"
   )
   AND p.license_plate IN (
      SELECT license_plate
      FROM bakery_security_logs
      WHERE month = 7
         AND day = 28
         AND hour = 10
         AND minute > 14
         AND minute < 26
   )
   )
   AND ph.day = 28
   AND ph.month = 7
   AND ph.duration < 60;

-- Seeing which flight the thief took and where was the destination
SELECT city
FROM flights fg
JOIN airports ao ON ao.id = fg.destination_airport_id
WHERE fg.id IN (
   SELECT id
   FROM flights
   WHERE month = 7
      AND day = 29
      ORDER BY hour, minute
      LIMIT 1
   );
