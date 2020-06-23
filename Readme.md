## flask代码生成模板说明

```python
"""
项目说明:
	本项目为减少开发带来的繁琐使用，通过读取数据库字段和表的注释文件，结合前端模板文件，生成对应单表操作的增删改查功能的实现，减少代码对单表操作的时间和效率。
"""
```

```python
"""
数据库要求说明:
	字段说明:每张数据表必须存在id字段，用来表示数据的唯一性.如(id,username,password,sex,gender,……………………);
	每张表都要有comments描述:描述的内容格式为 xx表:	   {"list":"username,password,sex,gender","edit":"username,password","search":"username,sex,gender"}
	list:用于展示页面的展示标题字段，如果没有指定的字段，就要渲染全部的数据字段.
	edit:用于操作编辑页面的数据展示，可修改字段的值.
	search:用户页面展示数据，并能够查询的查询条件字段.
"""
```

