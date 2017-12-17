from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class EsquemaManager(BaseDatabaseSchemaEditor):

    def eliminar_columna(self, modelo, campo):
        sql = self.sql_delete_column % {
            "table": self.quote_name(modelo._meta.db_table),
            "column": self.quote_name(campo),
        }
        self.execute(sql)