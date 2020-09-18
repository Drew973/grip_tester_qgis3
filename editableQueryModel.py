
#class to display and edit sqltable
# table needs primary key.

#use Pk for update
# and delete


class editableQueryModel(QSqlQueryModel)

	def setData:

	def setQuery():
		QSqlQueryModel



	def setTable(self,table)


	def setPk(self,Pk):




#SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
#FROM   pg_index i
#JOIN   pg_attribute a ON a.attrelid = i.indrelid
 #                    AND a.attnum = ANY(i.indkey)
#WHERE  i.indrelid = 'tablename'::regclass
#AND    i.indisprimary;