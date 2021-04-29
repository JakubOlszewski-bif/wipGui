# wipGui

Celem tej pracy magisterskiej jest stworzenie interfejsu graficznego dla narzędzi qiime2.

Nie zezwalam na udostępnianie i pobieranie kodu źródłowego bez mojej zgody.

I do not permit sharing or copying the source code without my consent.


## INSTRUKCJA URUCHOMIENIA

Program uruchamia się włączając moduł `mainMenu.py` w powłoce bash. Wszelkie prace w qiime2 wykonuje się również w tym module.   
Aby program uruchomił się poprawnie, wszystkie moduły (tzn. `mainMenu.py`, `commandWig.py`, `importable.py` oraz `winBuilder.py`) muszą znajdować się w tym samym katalogu.   
Do uruchomienia interfejsu graficznego **nie jest potrzebny** zainstalowany pakiet qiime2, ale bez tego pakietu próba wykonania polecenia zakończy się błędem.   

## INSTRUKCJA OBSŁUGI

### URUCHAMIANIE POJEDYNCZYCH POLECEŃ  

W Main Menu w lewym górnym rogu znajduje się lista `Commands` z zaimplementowanymi komendami *qiime2*. Aby uruchomić pojedyncze polecenie należy wybrać komendę z listy `Commands`, w ukazanym oknie dialogowym uzupełnić argumenty (wymagane jest uzupełnienie wszystkich argumentów w karcie `Required`), zaznaczenie przełącznika `'Proceed' runs the command` a następnie wciśnięcie przycisku `Proceed`. Okno dialogowe zostanie zamknięte, w Main Menu pojawi się komunikat o rozpoczęciu polecenia, a po jego zakończeniu, komunikat o tym czy polecenie zakończyło się sukcesem czy nie.  

### DODAWANIE POLECEŃ DO PIPELINE'U  

Aby dodać polecenie do pipeline'u należy wykonać wszystkie kroki z rozdziału **URUCHAMIANIE POJEDYNCZYCH POLECEŃ** (jeżeli nie chcemy by polecenie zostało wykonane, możemy odznaczyć przełącznik `'Proceed' runs the command`) a po zamknięciu okna dialogowego przez przycisk `Proceed`, w Main Menu należy wcisnąć przycisk `Add last command to pipeline`.  

### URUCHAMIANIE PIPELINE'U  

Po dodaniu poleceń do pipeline'u (lub wczytaniu wcześniej zapisanego pipeline'u) należy wcisnąć przysik `Run` aby uruchomić wszystkie polecenia w pipeline po kolei zaczynając od pierwszego. Jeżeli chcemy zacząć od innego polecenia w pipeline, należy jednokrotnie kliknąć na nie lewym przyciskiem myszy (LPM) w oknie pipeline'u a następnie zaznaczyć przełącznik `From selected` obok przycisku `Run`.  

### EDYCJA POLECEŃ W PIPELINE  

Jeżeli chcemy **edytować wartości argumentów** wewnątrz poleceń w pipeline, należy rozwinąć interesujące nas polecenie klikając dwukrotnie LPM lub jednokrotnie na znak `+` obok nazwy polecenia. Nastepnie należy kliknąć dwukrotnie LPM na interesujący nas argument po czym wyświetli się okno edytowania w którym możemy zmienić wartość argumentu. Po zakończeniu edycji należy wyjść z okna edytowania klikając `Save` jeżeli chcemy zachować zmiany.  

Możliwa jest również **zmiana kolejności** poleceń wewnątrz pipeline'u. Aby to zrobić należy zaznaczyć interesujące nas polecenie klikając jednokrotnie LPM a następnie klikając na przycisk `Move up` jeżeli chcemy przenieść polecenie do góry wewnątrz pipeline'u lub `Move down` jeżeli chcemy przenieść je w dół.  

Jeżeli chcemy **usunąć pojedyncze polecenie** z pipeline'u należy zaznaczyć interesujące nas polecenie klikając jednokrotnie LPM a nastepnie wcisnąć przycisk `Delete`.  

Jeżeli chcemy **usunąć wszystkie polecenia** z pipeline'u należy wcisnąć przycisk `Delete all`.   

### ZAPISYWANIE PIPELINE'U DO PLIKU

Jeżeli chcemy zapisać utworzony pipeline do pliku, należy wcisnąć przycisk `Save` a w ukazanym oknie dialogowym należy wybrać katalog do zapisu oraz podać nazwę pliku. Pipeline jest zapisywany z rozszerzeniem .txt. 

### OTWIERANIE PIPELINE'U Z PLIKU

Jeżeli chcemy otworzyć wcześniej zapisany pipeline, należy wcisnąć przycisk `Open` a w uzyskanym oknie dialogowym należy wybrać plik w którym znajduje się zapisany pipeline.  
**Uwaga**: Pipeline jest zapisywany w specjalnym formacie tworzonym przez program. Przekazanie pliku z niewłaściwym formatem może spowodować nieoczekiwany błąd.
