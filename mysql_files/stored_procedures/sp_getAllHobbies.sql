CREATE PROCEDURE `sp_getAllHobbies` ()
BEGIN
	SELECT DISTINCT hobby_id, hobby_name FROM hobby;
END