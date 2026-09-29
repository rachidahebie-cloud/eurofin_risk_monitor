-- Volatilité moyenne 30j par secteur (banques vs assurances) sur les 12 derniers mois
-- (le secteur est défini dans src/config.py : à joindre via une table de référence à créer)

-- Drawdown maximum par valeur
SELECT ticker, MIN(drawdown) AS max_drawdown
FROM indicators
GROUP BY ticker
ORDER BY max_drawdown;

-- Dernier snapshot des indicateurs
SELECT i.*
FROM indicators i
JOIN (SELECT ticker, MAX(date) AS d FROM indicators GROUP BY ticker) m
  ON i.ticker = m.ticker AND i.date = m.d;

-- TODO : rendement moyen selon régime de taux BCE (hausse / baisse / stable) avec une CTE
