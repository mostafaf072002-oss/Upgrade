{
    'name': 'Real Estate System',
    'version': '1.0',
    'summary': 'Full Real Estate: Property, Owners, Customers, Sales, Rentals and Contracts',
    'description': """
        Complete Real Estate System for Odoo 14
        =============================================
        Features:
        - Property Management
        - Owners
        - Customers
        - Sales
        - Rentals
        - Contracts
        - Internal & External API
        - QWeb Reports
        - Wizards
        - Dashboards
        - Role-based Security
    """,
    'author': 'Mostafa Fawzy',
    'category': '',
    'depends': ['base', 'mail', 'web', 'board', 'account_accountant'],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'data/sequence.xml',
        'views/property_view.xml',
        'views/menu_views.xml',
        'views/assets.xml',
    ],

    'qweb': [
        'static/src/components/xml/property_dashboard.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
