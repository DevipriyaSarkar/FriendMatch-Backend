CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addFriend`(
	IN p_user_id1 BIGINT,
    IN p_user_id2 BIGINT
)
BEGIN
	IF ( 
		SELECT NOT EXISTS (SELECT 1 FROM user WHERE user_id = p_user_id1) AND
		NOT EXISTS (SELECT 1 FROM user WHERE user_id = p_user_id2)
        ) 
    THEN
		SELECT 'Either or both user do not exist !!';
     
    ELSE
		INSERT INTO user_friend
		(
			id,
			friend_id
		)
		VALUES
		(
			p_user_id1,
			p_user_id2
		);
        
	END IF;
END