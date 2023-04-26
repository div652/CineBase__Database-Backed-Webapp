----- master: title, ratings -----
\set u_title '\'Pirates of the Caribbean\''
\set u_titleType '\'movie\''
\set u_startYear 2000
\set u_endYear 2010
\set u_isAdult NULL
\set u_runtime NULL
\set u_genres NULL
\set u_cutOrIn false
\set u_averageRating 7.5
\set u_numVotes 10

Select *
From title natural join ratings
Where (:u_title is NULL or lower(trim(primarytitle)) LIKE lower('%' || :u_title || '%') or lower(trim(originaltitle)) LIKE lower('%' || :u_title || '%'))
	and (:u_titleType is NULL or lower(titletype) = lower(:u_titleType))
	and (:u_startYear is NULL or startyear >= :u_startYear)
	and (:u_endYear is NULL or endyear is NULL or endyear <= :u_endYear)
	and (:u_isAdult is NULL or isadult = :u_isAdult)
	and (:u_runtime is NULL or runtime <= :u_runtime)
	and (:u_genres is NULL or (:u_cutOrIn = true and :u_genres & genres > 0) or (:u_cutOrIn = false and :u_genres & genres = :u_genres))
    and (:u_numVotes is NULL or numVotes>= :u_numVotes)
    and (:u_averageRating is NULL or averageRating>= :u_averageRating)
ORDER BY averageRating DESC, numVotes DESC;


----- master: persons, principal, title, ratings ------
\set u_title NULL
\set u_startYear 1980
\set u_numTitles 20
\set u_celeb '\'Christopher Nolan\''
\set u_category '\'director\''

Select title.*, averageRating
From persons natural join principals natural join title natural join ratings
Where (primaryName= :u_celeb)
    and (:u_category is NULL or category= :u_category)
    and (:u_title is NULL or lower(trim(primarytitle)) LIKE lower('%' || :u_title || '%') or lower(trim(originaltitle)) LIKE lower('%' || :u_title || '%'))
	and (:u_titleType is NULL or lower(titletype) = lower(:u_titleType))
 	and (:u_startYear is NULL or startyear >= :u_startYear)
 	and (:u_endYear is NULL or endyear is NULL or endyear <= :u_endYear)
	and (:u_isAdult is NULL or isadult = :u_isAdult)
	and (:u_runtime is NULL or runtime <= :u_runtime)
	and (:u_genres is NULL or (:u_cutOrIn = true and :u_genres & genres > 0) or (:u_cutOrIn = false and :u_genres & genres = :u_genres))
    and (:u_numVotes is NULL or numVotes>= :u_numVotes)
    and (:u_averageRating is NULL or averageRating>= :u_averageRating)
ORDER BY averageRating DESC, numVotes DESC
LIMIT CASE WHEN :u_numTitles is not null THEN :u_numTitles ELSE 100 END;

----- debut movie of given actor -----
\set u_actor '\'Tom Hanks\''
select primaryName, primaryTitle, originaltitle
from persons natural join principals natural join title
where primaryName= :u_actor and (category='actor' or category='actress') and titleType='movie'
order by startYear
limit 1;

----- debut movies of all actors -----
select primaryName, primaryTitle
from (
 select personid, primaryName, primaryTitle, row_number() over(partition by personid order by startYear asc) as row_num
 from persons natural join principals natural join titl
 where (category='actor' or category='actress') and titleType='movie'
) as T
where row_num=1;

----- celebs born in the same year as curr_user -----
\set u_birthdate 'date ''1980-04-01'''
select primaryName
from persons
where birthYear = date_part('year', :birthdate);

----- favorite actor -----
\set u_emailid '\'tombrown@hotmail.com\''
select primaryName as myFavActor
from rated natural join principals natural join persons
where emailid = :u_emailid and (category='actor')
group by personid, primaryName
order by sum(rating) DESC
limit 1;
----- favorite actress -----
\set u_emailid '\'johndoe@gmail.com\''
select primaryName as myFavActress
from rated natural join principals natural join persons
where emailid = :u_emailid and (category='actress')
group by personid, primaryName
order by sum(rating) DESC
limit 1;

----- most popular celebs of all time -----
select primaryName as mostPopularCeleb 
from persons natural join principals natural join ratings
group by personid, primaryName, titleid
order by sum(averageRating*numVotes) DESC
limit 10;

----- most popular movies/series of all time -----
select primarytitle as name, averagerating as rating
from title natural join ratings
where averageRating is not NULL
order By (averageRating * numVotes) DESC
limit 10;


----- Genre Based Recomendation -----
CREATE OR REPLACE FUNCTION calculate_genre_scores(curr_user VARCHAR) 
RETURNS INTEGER[] AS $$
DECLARE
    genre_scores INTEGER[];
    rec record;
    ind INTEGER;
BEGIN
    -- SELECT curr_user INTO user_id;
    CREATE TEMP VIEW ratedxtitle AS
    SELECT r.emailid, t.titleid, r.rating, t.genres
    FROM rated r Join title t On r.titleid = t.titleid;

    -- initialize the array with zeros
    genre_scores := array_fill(0, ARRAY[32]);

    -- loop over the tuples
    FOR rec IN SELECT * FROM ratedxtitle rt where rt.emailid = curr_user LOOP
        FOR ind IN 0..31 LOOP
            IF ((rec.genres >> ind) & 1) = 1 THEN
                -- added 1 because it was 1 indexed array
                genre_scores[ind+1] := genre_scores[ind+1] + rec.rating;
            END IF;
        END LOOP;
    END LOOP;

    -- return the array
    DROP VIEW ratedxtitle;
    RETURN genre_scores;
END $$ LANGUAGE plpgsql;

\set u_emailid '\'amy.johnson@hotmail.com\''
select calculate_genre_scores(:u_emailid);

--genre scores for all users--
select emailid, calculate_genre_scores(emailid)
from users 
--where emailid = :u_emailid
;


CREATE OR REPLACE FUNCTION calculate_score(genre INTEGER, genre_scores INTEGER[])
RETURNS INTEGER AS $$
DECLARE
    score INTEGER := 0;
    ind INTEGER;
BEGIN
    -- loop over the tuples
    -- RAISE NOTICE 'Genre scores: %', genre_scores;
    FOR ind IN 0..31 LOOP
        IF ((genre >> ind) & 1) = 1 THEN
            score := score + genre_scores[ind + 1];
            -- RAISE NOTICE 'new score: %', score;
        END IF;
    END LOOP;
    -- return the score
    RETURN score;
END $$ LANGUAGE plpgsql;

-- DO $$
-- DECLARE
--     genre_scores INTEGER[];
--     curr_user VARCHAR := 'mohammed.ali@yahoo.com';
-- BEGIN
--     SELECT calculate_genre_scores(curr_user) INTO genre_scores;
--     -- RAISE NOTICE 'Genre scores: %', genre_scores;
--     SELECT count(*), calculate_score(t.genres, genre_scores) as score
--     FROM title t
--     ORDER BY score DESC
--     LIMIT 5;
-- END $$;
-- Select * from res;


----- master: episodes -----
\set s_num_start  1
\set s_num_end 1
\set ep_num_start 1
\set ep_num_end 1
\set min_eps   5  
\set max_eps   10

with 
    totEpFilter as(
    select parenttitleid 
    from episode 
    group by parenttitleid 
    having count(*) >= :min_eps and count(*) < :max_eps
    ), 
    required_series_filter as(
    select titleid
    from episode
    where parenttitleid in (select * from totEpFilter)
    )
select * From episode t 
where 
(:s_num_start= -1 or t.seasonNumber >= :s_num_start)
and (:s_num_end = -1 or t.seasonNumber <= :s_num_end)
and (:ep_num_start= -1 or t.episodeNumber >= :ep_num_start)
and (:ep_num_end = -1 or t.episodeNumber <= :ep_num_end)
and (:min_eps=0 AND :max_eps=100000)
UNION
select * From episode t 
where 
(:s_num_start= -1 or t.seasonNumber >= :s_num_start)
and (:s_num_end = -1 or t.seasonNumber <= :s_num_end)
and (:ep_num_start= -1 or t.episodeNumber >= :ep_num_start)
and (:ep_num_end = -1 or t.episodeNumber <= :ep_num_end)
and (  t.titleid in (select * from required_series_filter));
