
from typing import Any
from django import forms
from .models import Operation, Category, BankAccount
from budget.logic.queries import get_all_category, get_all_bank_accounts


class BankAccountForm(forms.ModelForm):
    
    name = forms.CharField(label="Имя счета")
    bank = forms.CharField(label="Банк")
    
    class Meta:
        model = BankAccount
        fields = ("name", "bank")
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["bank"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["name"].widget.attrs["placeholder"] = "Имя счета"
        self.fields["bank"].widget.attrs["placeholder"] = "Имя банка"


class OperationForm(forms.ModelForm):
    operation_date = forms.DateField()
    category = forms.ModelChoiceField(queryset=get_all_category())
    bank_account = forms.ModelChoiceField(queryset=get_all_bank_accounts())
    amount = forms.DecimalField()
    operation_type = forms.ChoiceField(label="Тип категории", choices=Operation.OPER_TYPE_CHOICES)
    comment = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Operation
        fields = ("operation_date", "category", "bank_account", "operation_type", "amount", "comment")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["operation_date"].widget = forms.widgets.DateInput(
            format = ('%Y-%m-%d'),
            attrs={
                "type": "date",
                "placeholder": "yyyy-mm-dd (DOB)",
                "class": "form-control",
                "autocomplete": "off"
            }
        )
        self.fields["category"].widget.attrs["class"] = "form-control"
        self.fields["amount"].widget.attrs["class"] = "form-control"
        self.fields["bank_account"].widget.attrs["class"] = "form-control form-select"
        self.fields["operation_type"].widget.attrs["class"] = "form-select form-select"
        self.fields["comment"].widget.attrs["class"] = "form-control"

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя категории",
        max_length=20,
        required=True
    )
    limit = forms.DecimalField(decimal_places=2, max_digits=8, required=False)

    class Meta:
        model = Category
        fields = ("name", "limit")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["name"].widget.attrs["placeholder"] = "Имя категории"
        self.fields["limit"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["limit"].widget.attrs["placeholder"] = "Лимит за период"
        
