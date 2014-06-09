# How often are data types reused? answer: not very often
SELECT datasets_datatype.name, count(*) AS count
FROM datasets_dataset
JOIN datasets_datatype ON (datasets_datatype.id = datasets_dataset.data_type_id)
GROUP BY datasets_datatype.name
ORDER BY count DESC;

# How well are data sets distributed?
SELECT datasets_datagroup.name, count(*) AS count
FROM datasets_dataset
JOIN datasets_datagroup ON (datasets_datagroup.id = datasets_dataset.data_group_id)
GROUP BY datasets_datagroup.name
ORDER BY count DESC;

# What data types are there in a given data group?
SELECT datasets_datatype.name
FROM datasets_datagroup
JOIN datasets_dataset ON (datasets_datagroup.id = datasets_dataset.data_group_id)
JOIN datasets_datatype ON (datasets_datatype.id = datasets_dataset.data_type_id)
WHERE datasets_datagroup.name = 'carers-allowance';

# Same for all data groups
SELECT datasets_datagroup.name as data_group, datasets_datatype.name as data_type
FROM datasets_datagroup
JOIN datasets_dataset ON (datasets_datagroup.id = datasets_dataset.data_group_id)
JOIN datasets_datatype ON (datasets_datatype.id = datasets_dataset.data_type_id)
ORDER BY datasets_datagroup.name, datasets_dataset.name;
