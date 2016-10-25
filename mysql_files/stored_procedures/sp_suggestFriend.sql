CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_suggestFriend`(
    p_user_id INT
)
BEGIN
	(SELECT DISTINCT USER.id, USER.user_name, USER.age, USER.gender
    FROM user_details USER, user_hobby HOBBY1
    WHERE USER.id = HOBBY1.id AND
		USER.id <> p_user_id AND
		HOBBY1.hobby IN
			(SELECT hobby FROM user_hobby WHERE id = p_user_id) AND
		USER.id NOT IN
			(SELECT friend_id FROM user_friend
            WHERE id = p_user_id)
	)
	UNION
    (SELECT DISTINCT USER.id, USER.user_name, USER.age, USER.gender
    FROM user_details USER, user_hobby HOBBY1
    WHERE USER.id = HOBBY1.id AND
		HOBBY1.hobby IN
			(
				SELECT related_hobby FROM hobby
                WHERE hobby_name IN
					(SELECT hobby FROM user_hobby WHERE id = p_user_id)
			) AND
		USER.id NOT IN
			(SELECT friend_id FROM user_friend
            WHERE id = p_user_id)
	);
END