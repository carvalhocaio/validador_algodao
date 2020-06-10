from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (NotaFiscal,
                      Abastecimento,
                      OSAutomotiva,
                      AbastecimentoItem,
                      OSAgricola,
                      ApontamentoProducao,
                      InsumoGin,
                      Pedido)


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class TokenFilter(InputFilter):
    parameter_name = 'token'
    title = _('Token')

    def queryset(self, request, queryset):
        if self.value() is not None:
            token = self.value()

            return queryset.filter(token__icontains=token)


@admin.register(InsumoGin)
class InsumoGinAdmin(admin.ModelAdmin):
    list_filter = (TokenFilter, 'status', 'data', 'operacao',)
    list_display = ['token',
                    'wsdl_retorno',
                    'operacao',
                    'data',
                    'tempo_processamento',
                    'status', ]

@admin.register(ApontamentoProducao)
class ApontamentoProducaoAdmin(admin.ModelAdmin):
    list_filter = (TokenFilter, 'status', 'data', 'operacao',)
    list_display = ['token',
                    'wsdl_retorno',
                    'operacao',
                    'data',
                    'tempo_processamento',
                    'status', ]


@admin.register(OSAutomotiva)
class OSAutomotivaAdmin(admin.ModelAdmin):
    list_filter = (TokenFilter, 'status', 'data', 'operacao', )
    list_display = ['token',
                    'wsdl_retorno',
                    'operacao',
                    'data',
                    'tempo_processamento',
                    'status', ]


@admin.register(OSAgricola)
class OSAgricolaAdmin(admin.ModelAdmin):
    list_filter = (TokenFilter, 'status', 'data', 'operacao',)
    list_display = ['token',
                    'wsdl_retorno',
                    'operacao',
                    'data',
                    'tempo_processamento',
                    'status', ]


class AbastecimentoItemTabed(admin.StackedInline):
    model = AbastecimentoItem


@admin.register(Abastecimento)
class AbastecimentoAdmin(admin.ModelAdmin):
    inlines = [AbastecimentoItemTabed, ]
    list_filter = (TokenFilter, 'status', 'data', 'operacao',)
    list_display = ['token',
                    'wsdl_retorno',
                    'operacao',
                    'data',
                    'tempo_processamento',
                    'status', ]


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_filter = (TokenFilter, 'status', 'data', 'operacao',)
    list_display = ['token',
                    'wsdl_retorno',
                    'operacao',
                    'data',
                    'tempo_processamento',
                    'status', ]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_filter = (TokenFilter, 'status', 'data', 'operacao',)
    list_display = ['token',
                    'wsdl_retorno',
                    'operacao',
                    'data',
                    'tempo_processamento',
                    'status', ]

