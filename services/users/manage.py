import unittest, coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User


COV = coverage.coverage(
    branch=True,
    include="project/*",
    omit=[
        "project/test/*",
        "project/config.py",
    ],
)

COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("test")
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command("seed_db")
def seed_db():
    """Seed the db with initial data"""
    db.session.add(User(username="testuser", email="testuser@gmail.com"))
    db.session.add(User(username="testuser2", email="testuser2@gmail.com"))
    db.session.commit()


@cli.command()
def cov():
    """
    Runs the unit tests coverage
    """
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    cli()
