from odoo import api, fields, models, _
from num2words import num2words


class ReportReceiptVoucherAccountView(models.AbstractModel):
    _name = "report.bi_print_journal_entries.report_receipt_voucher2"
    _description = "Receipt Voucher"

    def ComputeAmountInWords(self, amount, docids):
        payment = self.env['account.move'].search([('id', '=', docids)])

        amount_word_ar = ""
        decimal_part = amount % 1

        # تحويل الرقم إلى كلمات
        amount_word_ar = num2words(int(amount), lang='ar')

        # معالجة الحالات الخاصة
        amount_word_ar = amount_word_ar.replace("فاصله", " و ").replace("فاصلة", " و ")
        amount_word_ar = amount_word_ar.replace("جنيه", "جنيهات ")
        amount_word_ar = amount_word_ar.replace("مئتين", "مائتين").replace("مئتان", "مائتين")
        amount_word_ar = amount_word_ar.replace("ثلاثة مئة", "ثلاثمائة").replace("أربعة مئة", "أربعمائة")
        amount_word_ar = amount_word_ar.replace("خمسة مئة", "خمسمائة").replace("ستة مئة", "ستمائة")
        amount_word_ar = amount_word_ar.replace("سبعة مئة", "سبعمائة").replace("ثمانية مئة", "ثمانمائة")
        amount_word_ar = amount_word_ar.replace("تسعة مئة", "تسعمائة")

        # منع إضافة "و" بعد الأرقام المئوية الكاملة
        if amount not in [100, 200, 300, 400, 500, 600, 700, 800, 900]:
            amount_word_ar = amount_word_ar.replace("ئة", "ئة و ")

        # تنظيف الفواصل والمسافات الزائدة
        amount_word_ar = amount_word_ar.replace('  ', ' ').replace(',', ' و ').replace('.', ' و ')
        amount_word_ar = amount_word_ar.replace('و و و', ' و ').replace('و و', ' و ')

        # إضافة العملة المناسبة
        currency_map = {
            "AED": " درهم اماراتي ",
            "EGP": " جنيه مصري ",
            "EUR": " يورو ",
            "SAR": " ريال سعودي ",
            "USD": " دولار امريكي "
        }
        amount_word_ar += currency_map.get(payment.currency_id.name, "")

        # تحويل الجزء العشري إن وجد
        if decimal_part > 0:
            decimal_part_ar = num2words(int(decimal_part * 100), lang='ar')  # تحويل القروش
            decimal_part_ar = decimal_part_ar.replace(',', ' و ')
            amount_word_ar += decimal_part_ar + " قرشاً "

        amount_word_ar += " فقط لا غير "

        return amount_word_ar
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        domains = []
        in_out = 0
        payment = self.env['account.move'].search([('id', '=', docids)])
        label = ''
        for line in payment.line_ids:
            if "Cash Main" in line.account_id.name:
                label = line.name
            if "Bank Main" in line.account_id.name:
                label = line.name
        # unit_reservation = self.env['unit.reservation'].search([('journal_entry.name', '=', payment.name)])
        # print("unit_reservation", unit_reservation.id)
        cheque_number = ".................................."
        cheque_or_not = "نقدى"
        bank_name = ".................................."
        cheque_date = ".................................."
        if payment.payment_type == "cheque":
            cheque_number = payment.cheque_no
            cheque_or_not = "شيك"
            bank_name = payment.bank_id.name
            cheque_date = payment.cheque_date
        elif payment.payment_type == "bank_transfer":
            cheque_or_not = "تحويل بنكى"
            bank_name = payment.bank_id.name
        elif payment.payment_type == "visa":
            cheque_or_not = "فيزا"
            bank_name = payment.bank_id.name

        if payment.in_out == "out":
            in_out = -1
        elif payment.in_out == "out":
            in_out = 1
        else:
            in_out = 1
        return {
            'name': payment.name,
            'receipt_num': payment.receipt_num,
            'payment_type': payment.payment_type,
            'payment_date': payment.date,
            'payment_amount': "{:,}".format(abs(payment.line_ids[0].amount_currency)).rstrip('0').rstrip('.'),
            'payment_amount_words': self.ComputeAmountInWords(abs(payment.line_ids[0].amount_currency), docids),

            'partner_name': payment.line_ids[0].partner_id.name,
            'user1':  payment.create_uid.name,
            'text_free': payment.text_free,
            'ref': payment.ref,
            'cheque_no': cheque_number,
            'cheque_or_not': cheque_or_not,
            'bank_name': bank_name,
            'cheque_date': cheque_date,
            'unit': payment.unit.name,
            'currency_rate': format(payment.line_ids[0].debit * in_out, ","),
            'currency': payment.line_ids[0].currency_id.name,
            'project': payment.project_id.name,
            'label': label

            # 'docs': docs,
        }
