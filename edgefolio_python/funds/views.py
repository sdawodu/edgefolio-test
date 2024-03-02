from django.shortcuts import render
from rest_framework import viewsets, renderers
from .serializers import FundSerializer
from .models import Fund

class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    renderer_classes = [renderers.JSONRenderer, renderers.TemplateHTMLRenderer]
    template_name = 'funds/fund_list.html'

    def get_queryset(self):
        queryset = Fund.objects.all()
        strategy = self.request.query_params.get('strategy')
        if strategy is not None:
            queryset = queryset.filter(strategy=strategy)
        return queryset


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Serve HTML if requested, otherwise serve JSON
        if request.accepted_renderer.format == 'html':
            return render(
                request, self.template_name,
                {'funds': response.data, 'sum': sum([fund['aum'] for fund in response.data])})
        return response