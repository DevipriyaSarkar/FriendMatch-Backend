CREATE PROCEDURE `sp_showRelatedHobby`(
    IN p_user_id1 BIGINT,
    IN p_user_id2 BIGINT
)
BEGIN
	SELECT R.related_hobby_id, H.hobby_name 
    FROM related_hobby R, hobby H
    WHERE H.hobby_id = R.related_hobby_id AND
		R.hobby_id IN
		( 
			SELECT UH.hobby_id FROM user_hobby UH
			WHERE UH.id = p_user_id1
		) AND
        R.related_hobby_id IN
        (
			SELECT UH.hobby_id FROM user_hobby UH
			WHERE UH.id = p_user_id2
        );
END