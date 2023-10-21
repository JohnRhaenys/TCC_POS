CRITICAL_DATES_QUERY = """
SELECT
DISTINCT
'Data Critica' AS contexto,
products.id AS productId,
products.description AS nomeProduto,
brands.name AS nomeMarca,
industries.document AS cnpjIndustria,
industries.social_reason AS razaoSocialIndustria,
industries.trade_name AS nomeFantasiaIndustria,
critical_dates.updated_at AS dataRegistroResposta,
critical_dates.date AS dataCritica,
critical_dates.quantity AS quantidade,
critical_dates.measure AS medida,
critical_dates.batch AS lote,
stores.id AS storeId,
stores.name AS nomeLoja,
flags.name AS nomeBandeira,
networks.name AS nomeRede
FROM critical_dates 
INNER JOIN questions_answers qa 
	ON qa.id = critical_dates.question_answer_id
INNER JOIN contract_products cp ON cp.id = qa.product_id
INNER JOIN products ON products.id = cp.products_id
INNER JOIN brands ON brands.id = products.brands_id
INNER JOIN industries ON industries.id = brands.industries_id
INNER JOIN stores ON stores.id = cp.stores_id
INNER JOIN flags ON flags.id = stores.flags_id
INNER JOIN networks ON networks.id = flags.networks_id
WHERE critical_dates.measure IS NOT NULL
AND stores.id NOT IN (
    SELECT id FROM stores WHERE name LIKE '%Loja Treinamento%'
);
"""


STOCK_COUNT_QUERY = """
SELECT
	DISTINCT
    'Contagem de Estoque' AS contexto,
    products.id AS productId,
    products.description AS nomeProduto,
    brands.name AS nomeMarca,
    industries.document AS cnpjIndustria,
    industries.social_reason AS razaoSocialIndustria,
    industries.trade_name AS nomeFantasiaIndustria,
    DATE(stock_count.updated_at) AS dataRegistroResposta,
    qa.value AS quantidadeEstoque,
    stock_count.measure AS medida,
    stores.id AS storeId,
    stores.name AS nomeLoja,
    flags.name AS nomeBandeira,
    networks.name AS nomeRede
FROM stock_count
INNER JOIN questions_answers qa
    ON qa.id = stock_count.question_answer_id
INNER JOIN contract_products cp ON cp.id = qa.product_id
INNER JOIN products ON products.id = cp.products_id
INNER JOIN brands ON brands.id = products.brands_id
INNER JOIN industries ON industries.id = brands.industries_id
INNER JOIN stores ON stores.id = cp.stores_id
INNER JOIN flags ON flags.id = stores.flags_id
INNER JOIN networks ON networks.id = flags.networks_id
JOIN (
    SELECT
        MIN(LEAST(critical_dates.updated_at, critical_dates.date)) AS minDate,
        MAX(GREATEST(critical_dates.updated_at, critical_dates.date)) AS maxDate
    FROM critical_dates 
    INNER JOIN questions_answers qa 
        ON qa.id = critical_dates.question_answer_id
    INNER JOIN contract_products cp ON cp.id = qa.product_id
    INNER JOIN products ON products.id = cp.products_id
    INNER JOIN brands ON brands.id = products.brands_id
    INNER JOIN industries ON industries.id = brands.industries_id
    INNER JOIN stores ON stores.id = cp.stores_id
    INNER JOIN flags ON flags.id = stores.flags_id
    INNER JOIN networks ON networks.id = flags.networks_id
    WHERE critical_dates.measure IS NOT NULL
    AND stores.name NOT LIKE '%Loja Treinamento%'
) AS date_range
ON DATE(qa.updated_at) BETWEEN date_range.minDate AND date_range.maxDate
AND stores.id NOT IN (
    SELECT id FROM stores WHERE name LIKE '%Loja Treinamento%'
);
"""


RUPTURE_QUERY = """
SELECT
DISTINCT
'Ruptura' AS contexto,
products.id AS productId,
products.description AS nomeProduto,
brands.name AS nomeMarca,
industries.document AS cnpjIndustria,
industries.social_reason AS razaoSocialIndustria,
industries.trade_name AS nomeFantasiaIndustria,
DATE(qa.updated_at) AS dataRegistroResposta,
stores.id AS storeId,
stores.name AS nomeLoja,
flags.name AS nomeBandeira,
networks.name AS nomeRede
FROM questions_answers qa
INNER JOIN attendance_answers aa
	ON aa.id = qa.attendance_answers_id
INNER JOIN contract_products cp ON cp.id = qa.product_id
INNER JOIN contract_tasks
ON contract_tasks.id = aa.answer_id
INNER JOIN tasks ON tasks.id = contract_tasks.tasks_id
INNER JOIN products ON products.id = cp.products_id
INNER JOIN brands ON brands.id = products.brands_id
INNER JOIN industries ON industries.id = brands.industries_id
INNER JOIN stores ON stores.id = cp.stores_id
INNER JOIN flags ON flags.id = stores.flags_id
INNER JOIN networks ON networks.id = flags.networks_id
JOIN (
SELECT
MIN(LEAST(critical_dates.updated_at, critical_dates.date)) AS minDate,
MAX(GREATEST(critical_dates.updated_at, critical_dates.date)) AS maxDate
FROM critical_dates
INNER JOIN questions_answers qa
ON qa.id = critical_dates.question_answer_id
INNER JOIN contract_products cp ON cp.id = qa.product_id
INNER JOIN products ON products.id = cp.products_id
INNER JOIN brands ON brands.id = products.brands_id
INNER JOIN industries ON industries.id = brands.industries_id
INNER JOIN stores ON stores.id = cp.stores_id
INNER JOIN flags ON flags.id = stores.flags_id
INNER JOIN networks ON networks.id = flags.networks_id
WHERE critical_dates.measure IS NOT NULL
AND stores.name NOT LIKE '%Loja Treinamento%'
) AS date_range
ON DATE(qa.updated_at) BETWEEN date_range.minDate AND date_range.maxDate
WHERE aa.answer_type = 'tasks'
AND stores.id NOT IN (
    SELECT id FROM stores WHERE name LIKE '%Loja Treinamento%'
);
"""