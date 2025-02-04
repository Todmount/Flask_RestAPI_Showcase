from core import db


def commit(obj):
    """
    Function for convenient commit
    """
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)
    return obj


class Model(object):
    @classmethod
    def create(cls, **kwargs):
        """
        Create new record

        cls: class
        kwargs: dict with object parameters
        """
        obj = cls(**kwargs)
        return commit(obj)

    @classmethod
    def update(cls, row_id, **kwargs):
        """
        Update record by id

        cls: class
        row_id: record id
        kwargs: dict with object parameters
        """
        obj = cls.query.filter_by(id=row_id).first()
        # return commit(obj)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            return commit(obj)
        return None  # If the record doesn't exist

    @classmethod
    def delete(cls, row_id):
        """
        Delete record by id

        cls: class
        row_id: record id
        return: int (1 if deleted else 0)
        """
        obj = cls.query.filter_by(id=row_id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return 1  # Successfully deleted
        return 0  # Record not found

    @classmethod
    def add_relation(cls, row_id, rel_obj):
        """
        Add relation to object

        cls: class
        row_id: record id
        rel_obj: related object
        """
        obj = cls.query.filter_by(id=row_id).first()
        if cls.__name__ == 'Actor':
            obj.filmography.append(rel_obj)
        elif cls.__name__ == 'Movie':
            obj.cast.append(rel_obj)
        return commit(obj)

    @classmethod
    def remove_relation(cls, row_id, rel_obj):
        """
        Remove certain relation

        cls: class
        row_id: record id
        rel_obj: related object
        """
        obj = cls.query.filter_by(id=row_id).first()
        if obj:
            if cls.__name__ == 'Actor' and rel_obj in obj.filmography:
                obj.filmography.remove(rel_obj)
            elif cls.__name__ == 'Movie' and rel_obj in obj.cast:
                obj.cast.remove(rel_obj)
            return commit(obj)
        return None  # Record not found

    @classmethod
    def clear_relations(cls, row_id):
        """
        Remove all relations by id

        cls: class
        row_id: record id
        """
        obj = cls.query.filter_by(id=row_id).first()
        if obj:
            if cls.__name__ == 'Actor':
                obj.filmography.clear()
            elif cls.__name__ == 'Movie':
                obj.cast.clear()
            return commit(obj)
        return None  # Record not found