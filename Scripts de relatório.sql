--Selecionar nome de usuário e associar ao acesso feito
SELECT b.first_name, a.sala_acesso, a.data_acesso FROM auth_user as b
INNER JOIN
(
	SELECT * 
	FROM monitoramento_registro
	
)AS a
ON b.id=a.usuario_id;

--Checar hora mais acessada
SELECT EXTRACT (HOUR FROM data_acesso) as Hora,COUNT(*) AS Quantidade
FROM monitoramento_registro
GROUP BY EXTRACT (HOUR FROM data_acesso)
ORDER BY Quantidade DESC
LIMIT 5;

--Checar hora menos acessada
SELECT EXTRACT (HOUR FROM data_acesso) as Hora,COUNT(*) AS Quantidade
FROM monitoramento_registro
GROUP BY EXTRACT (HOUR FROM data_acesso)
ORDER BY Quantidade ASC
LIMIT 10;

--Horas acessadas em ordem (pegar mais cedo e mais tarde)
SELECT to_char(data_acesso, 'HH24:MI') as Hora
FROM monitoramento_registro
ORDER BY Hora ASC;

--Checar dia mais acessado
SELECT EXTRACT (DAY FROM data_acesso) as Dia,COUNT(*) AS Quantidade
FROM monitoramento_registro
GROUP BY EXTRACT (DAY FROM data_acesso)
ORDER BY Quantidade DESC
LIMIT 5;


	
	
	