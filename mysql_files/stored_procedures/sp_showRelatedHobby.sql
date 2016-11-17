CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_showRelatedHobby`(
    p_user_id1 INT,
    p_user_id2 INT
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