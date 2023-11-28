import pytest
from main import app, db, Expense


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

def text_add_expense(client):
    response = client.post('/addexpense', data={
        'date': '2023-01-01',
        'expensename': 'Text Expense',
        'amount': 100,
        'category': 'Test Category'
    })

    assert response.status_code == 302
    assert response.location.endswith("/expenses")

    with app.app_context():
        expenses = Expense.query.all()
        assert len(expenses) == 1
        assert expenses[0].date == '2023-01-01'
        assert expenses[0].expense_name == 'Text Expense'
        assert expenses[0].amount == 100
        assert expenses[0].category == 'Test Category'

if __name__ == '__main__':
    pytest.main()