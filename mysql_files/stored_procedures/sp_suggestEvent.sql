CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_suggestEvent`(
    IN p_user_id BIGINT,
    IN p_date DATE
)
BEGIN
	(
		SELECT DISTINCT E.event_id, E.event_name, E.event_city, DATE(E.event_date)
		FROM `event` E, event_interest_group EG
		WHERE E.event_date > p_date AND
			EG.event_id = E.event_id AND
            EG.event_id NOT IN
            (
				SELECT DISTINCT event_id FROM user_event
                WHERE id = p_user_id
            ) AND
			EG.hobby_id IN
			(
				SELECT DISTINCT hobby_id FROM user_hobby
				WHERE id = p_user_id
			)
	)
	UNION
    (
		SELECT DISTINCT E.event_id, E.event_name, E.event_city, DATE(E.event_date)
		FROM `event` E, event_interest_group EG
		WHERE E.event_date > p_date AND
			EG.event_id = E.event_id AND
            EG.event_id NOT IN
            (
				SELECT DISTINCT event_id FROM user_event
                WHERE id = p_user_id
            ) AND
			EG.hobby_id IN
			(
				SELECT DISTINCT R.related_hobby_id FROM related_hobby R, user_hobby UH
				WHERE UH.hobby_id = R.hobby_id AND
					UH.id = p_user_id
			)
	);
END