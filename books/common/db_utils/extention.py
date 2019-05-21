from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert


@compiles(Insert)
def update_on_unique_key(insert, compiler, **kwargs):
    """
    kwargs:
        update_on_unique_key: bool
        exclude_keys: list. 当遇到duplicate key时不更新的键值
    """
    s = compiler.visit_insert(insert, **kwargs)
    exclude_keys = insert.kwargs.get('exclude_keys', [])
    exclude_keys.extend(['id', 'create_time', 'modify_time'])
    if insert.kwargs.get('update_on_unique_key'):
        fields = s[s.find("(") + 1:s.find(")")].replace(" ", "").split(",")
        generated_directive = ["{0}=VALUES({0})".format(field) for field in
                               fields if field not in exclude_keys]
        return s + " ON DUPLICATE KEY UPDATE " + ",".join(generated_directive)
    return s


def to_dict(self):
    column_name_list = [
        value[0] for value in self._sa_instance_state.attrs.items()
    ]
    return dict(
        (column_name, getattr(self, column_name)) for column_name in column_name_list
        if getattr(self, column_name, None) is not None
    )
