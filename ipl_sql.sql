create database ipl_2025
USE ipl_2025
show tables
#Query 1: Team with Most Wins
SELECT
    match_winner,
    COUNT(*) AS total_wins
FROM matches
GROUP BY match_winner
ORDER BY total_wins DESC;
#Query 2: Matches Hosted by Venue
SELECT
    venue,
    COUNT(*) AS matches_hosted
FROM matches
GROUP BY venue
ORDER BY matches_hosted DESC
#Query 3: Toss Impact
SELECT
ROUND(
    SUM(
        CASE
            WHEN toss_winner = match_winner
            THEN 1
            ELSE 0
        END
    ) * 100.0 / COUNT(*),
2
) AS toss_win_percentage
FROM matches
#Query 4: Top 10 Run Scorers
SELECT
    striker,
    SUM(runs_of_bat) AS total_runs
FROM deliveries
GROUP BY striker
ORDER BY total_runs DESC
LIMIT 10;
#Query 5: Top 10 Wicket Takers
SELECT
    bowler,
    COUNT(*) AS wickets
FROM deliveries
WHERE wicket_type IS NOT NULL
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;
#Query 6: Most Fours
SELECT
    striker,
    COUNT(*) AS fours
FROM deliveries
WHERE runs_of_bat = 4
GROUP BY striker
ORDER BY fours DESC
LIMIT 10;
#Query 7: Most Sixes
SELECT
    striker,
    COUNT(*) AS sixes
FROM deliveries
WHERE runs_of_bat = 6
GROUP BY striker
ORDER BY sixes DESC
LIMIT 10
#Query 8: Player of the Match Leaders
SELECT
    player_of_the_match,
    COUNT(*) AS awards
FROM matches
GROUP BY player_of_the_match
ORDER BY awards DESC;
#Query 9: Team-wise Total Runs
SELECT
    batting_team,
    SUM(runs_of_bat + extras) AS total_runs
FROM deliveries
GROUP BY batting_team
ORDER BY total_runs DESC;
#Query 10: Team-wise Wickets Lost
SELECT
    batting_team,
    COUNT(*) AS wickets_lost
FROM deliveries
WHERE wicket_type IS NOT NULL
GROUP BY batting_team
ORDER BY wickets_lost DESC;
#Advanced Query 1: Win Percentage by Team
SELECT
    team,
    matches_played,
    wins,
    ROUND((wins * 100.0 / matches_played), 2) AS win_rate
FROM
(
    SELECT
        team,
        COUNT(*) AS matches_played,
        SUM(win_flag) AS wins
    FROM
    (
        SELECT
            team1 AS team,
            CASE WHEN match_winner = team1 THEN 1 ELSE 0 END AS win_flag
        FROM matches

        UNION ALL

        SELECT
            team2 AS team,
            CASE WHEN match_winner = team2 THEN 1 ELSE 0 END AS win_flag
        FROM matches
    ) t
    GROUP BY team
) x
ORDER BY win_rate DESC;
#Advanced Query 2: Toss Winner Also Won Match
SELECT
    toss_winner,
    COUNT(*) AS toss_and_match_wins
FROM matches
WHERE toss_winner = match_winner
GROUP BY toss_winner
ORDER BY toss_and_match_wins DESC;
#Advanced Query 3: Best Strike Rate Batsmen
SELECT
    Batsman,
    Runs,
    Strike_rate
FROM orange_cap
WHERE Runs > 200
ORDER BY Strike_rate DESC;
#Advanced Query 4: Best Economy Bowlers
SELECT
    Bowler,
    Wickets,
    Economy_rate
FROM purple_cap
ORDER BY Economy_rate ASC;
#Advanced Query 5: Most Valuable Players
SELECT
    player_of_the_match,
    COUNT(*) AS awards
FROM matches
GROUP BY player_of_the_match
ORDER BY awards DESC;
