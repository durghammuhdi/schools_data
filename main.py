import csv
import os
import platform
import flet as ft

FILENAME = "schools_data.csv"
EXPORT_FILENAME = "تقرير_الإشراف_التربوي.csv"


def main(page: ft.Page):
  page.title = "نظام الإشراف التربوي - إدارات المدارس"
  page.theme_mode = ft.ThemeMode.LIGHT
  page.padding = 0

  editing_index = [-1]

  if not os.path.exists(FILENAME):
    with open(FILENAME, mode="w", newline="", encoding="utf-8-sig") as file:
      writer = csv.writer(file)
      writer.writerow([
          "المدرسة",
          "الاختصاص",
          "الملاك المطلوب",
          "العدد الحالي",
          "الحالة",
          "الفرق",
      ])

  def load_records():
    records = []
    if os.path.exists(FILENAME):
      with open(FILENAME, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
          if row and len(row) >= 6:
            records.append(row)
    return records

  def save_all_records(records):
    with open(FILENAME, mode="w", newline="", encoding="utf-8-sig") as file:
      writer = csv.writer(file)
      writer.writerow([
          "المدرسة",
          "الاختصاص",
          "الملاك المطلوب",
          "العدد الحالي",
          "الحالة",
          "الفرق",
      ])
      writer.writerows(records)

  card_total = ft.Text("0", size=22, weight=ft.FontWeight.BOLD, color="blue")
  card_vacant = ft.Text("0", size=22, weight=ft.FontWeight.BOLD, color="red")
  card_surplus = ft.Text(
      "0", size=22, weight=ft.FontWeight.BOLD, color="orange"
  )

  status_label = ft.Text(value="", color="green", size=14)

  txt_school = ft.TextField(
      label="اسم المدرسة", width=240, text_align=ft.TextAlign.RIGHT
  )
  txt_spec = ft.TextField(
      label="الاختصاص", width=220, text_align=ft.TextAlign.RIGHT
  )
  txt_req = ft.TextField(
      label="الملاك المطلوب",
      width=130,
      keyboard_type=ft.KeyboardType.NUMBER,
      text_align=ft.TextAlign.RIGHT,
  )
  txt_curr = ft.TextField(
      label="العدد الحالي",
      width=130,
      keyboard_type=ft.KeyboardType.NUMBER,
      text_align=ft.TextAlign.RIGHT,
  )

  data_table = ft.DataTable(
      columns=[
          ft.DataColumn(ft.Text("إجراءات", weight=ft.FontWeight.BOLD)),
          ft.DataColumn(ft.Text("الفرق", weight=ft.FontWeight.BOLD)),
          ft.DataColumn(ft.Text("الحالة", weight=ft.FontWeight.BOLD)),
          ft.DataColumn(ft.Text("الحالي", weight=ft.FontWeight.BOLD)),
          ft.DataColumn(ft.Text("الملاك", weight=ft.FontWeight.BOLD)),
          ft.DataColumn(ft.Text("الاختصاص", weight=ft.FontWeight.BOLD)),
          ft.DataColumn(ft.Text("المدرسة", weight=ft.FontWeight.BOLD)),
      ],
      rows=[],
  )

  def update_dashboard():
    records = load_records()
    total_schools = len(set([r[0].strip() for r in records if r[0].strip()]))
    vacant_count = sum(1 for r in records if r[4].strip() == "شاغر")
    surplus_count = sum(1 for r in records if r[4].strip() == "فيض")

    card_total.value = str(total_schools)
    card_vacant.value = str(vacant_count)
    card_surplus.value = str(surplus_count)

  def refresh_table(e=None):
    data_table.rows.clear()
    records = load_records()

    query_school = (
        txt_search_school.value.strip().lower()
        if txt_search_school.value
        else ""
    )
    selected_spec = (
        filter_dropdown.value
        if filter_dropdown.value and filter_dropdown.value != "الكل"
        else ""
    )

    for i, row in enumerate(records):
      idx = i
      r_data = row

      school_name = row[0].lower()
      spec_name = row[1].strip()

      if query_school and query_school not in school_name:
        continue

      if selected_spec and selected_spec != spec_name:
        continue

      data_table.rows.append(
          ft.DataRow(
              cells=[
                  ft.DataCell(
                      ft.Row([
                          ft.IconButton(
                              icon=ft.Icons.EDIT,
                              icon_color="blue",
                              tooltip="تعديل",
                              on_click=lambda e, idx=idx, r=r_data: start_edit(
                                  idx, r
                              ),
                          ),
                          ft.IconButton(
                              icon=ft.Icons.DELETE,
                              icon_color="red",
                              tooltip="حذف",
                              on_click=lambda e, idx=idx: delete_record(idx),
                          ),
                      ], alignment=ft.MainAxisAlignment.END)
                  ),
                  ft.DataCell(ft.Text(row[5])),
                  ft.DataCell(ft.Text(row[4])),
                  ft.DataCell(ft.Text(row[3])),
                  ft.DataCell(ft.Text(row[2])),
                  ft.DataCell(ft.Text(row[1])),
                  ft.DataCell(ft.Text(row[0])),
              ]
          )
      )
    update_dashboard()
    page.update()

  txt_search_school = ft.TextField(
      label="تصفية حسب المدرسة...",
      width=200,
      prefix_icon=ft.Icons.SEARCH,
      text_align=ft.TextAlign.RIGHT,
  )
  txt_search_school.on_change = refresh_table

  filter_dropdown = ft.Dropdown(
      label="تصفية حسب الاختصاص",
      width=200,
      value="الكل",
      options=[
          ft.dropdown.Option("الكل"),
          ft.dropdown.Option("حاسوب"),
          ft.dropdown.Option("رياضيات"),
          ft.dropdown.Option("طبيعيات"),
          ft.dropdown.Option("علوم"),
      ],
  )
  filter_dropdown.on_change = refresh_table

  def export_data_to_file(e):
    try:
      if platform.system() == "Android":
        # استخدام مجلد التخزين المؤقت المتاح للكتابة المباشرة على أندرويد دون مشاكل صلاحيات
        export_path = os.path.join(os.getcwd(), EXPORT_FILENAME)
      else:
        export_path = EXPORT_FILENAME

      records = load_records()
      with open(export_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([
            "المدرسة",
            "الاختصاص",
            "الملاك المطلوب",
            "العدد الحالي",
            "الحالة",
            "الفرق",
        ])
        writer.writerows(records)

      status_label.value = f"تم التصدير بنجاح: {export_path}"
      status_label.color = "green"
    except Exception as ex:
      status_label.value = f"حدث خطأ أثناء التصدير: {str(ex)}"
      status_label.color = "red"
    page.update()

  def start_edit(index, row_data):
    editing_index[0] = index
    txt_school.value = row_data[0]
    txt_spec.value = row_data[1]
    txt_req.value = row_data[2]
    txt_curr.value = row_data[3]
    btn_add.text = "تحديث السجل"
    btn_cancel.visible = True
    status_label.value = f"جاري تعديل: {row_data[0]}"
    status_label.color = "blue"
    page.update()

  def cancel_edit(e=None):
    editing_index[0] = -1
    txt_school.value = ""
    txt_spec.value = ""
    txt_req.value = ""
    txt_curr.value = ""
    btn_add.text = "إضافة سجل"
    btn_cancel.visible = False
    status_label.value = ""
    page.update()

  def delete_record(index):
    records = load_records()
    if 0 <= index < len(records):
      records.pop(index)
      save_all_records(records)
      refresh_table()
      status_label.value = "تم حذف السجل بنجاح!"
      status_label.color = "orange"
      page.update()

  def save_or_update(e):
    if (
        not txt_school.value
        or not txt_spec.value
        or not txt_req.value
        or not txt_curr.value
    ):
      status_label.value = "يرجى ملء جميع الحقول!"
      status_label.color = "red"
      page.update()
      return

    try:
      req = int(txt_req.value)
      curr = int(txt_curr.value)
    except ValueError:
      status_label.value = "الملاك والأعداد يجب أن تكون أرقاماً فقط!"
      status_label.color = "red"
      page.update()
      return

    diff = curr - req
    status = "شاغر" if diff < 0 else ("فيض" if diff > 0 else "مكتمل")
    new_row = [
        txt_school.value.strip(),
        txt_spec.value.strip(),
        str(req),
        str(curr),
        status,
        str(abs(diff)),
    ]

    records = load_records()

    if editing_index[0] != -1:
      records[editing_index[0]] = new_row
      save_all_records(records)
      status_label.value = "تم تحديث السجل بنجاح!"
      status_label.color = "green"
      cancel_edit()
    else:
      records.append(new_row)
      save_all_records(records)
      status_label.value = "تمت إضافة السجل بنجاح!"
      status_label.color = "green"
      cancel_edit()

    refresh_table()

  btn_add = ft.Button("إضافة سجل", on_click=save_or_update, icon=ft.Icons.ADD)
  btn_cancel = ft.Button(
      "إلغاء التعديل", on_click=cancel_edit, icon=ft.Icons.CLOSE, visible=False
  )
  btn_export = ft.Button(
      "تصدير التقرير",
      on_click=export_data_to_file,
      icon=ft.Icons.SAVE,
      color="green",
  )

  def make_stat_card(title, value_widget, icon_name, icon_color):
    return ft.Card(
        elevation=2,
        content=ft.Container(
            padding=15,
            width=200,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Icon(icon_name, color=icon_color, size=30),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            ft.Text(title, size=12, color="gray"),
                            value_widget,
                        ],
                    ),
                ],
            ),
        ),
    )

  stats_row = ft.Row(
      alignment=ft.MainAxisAlignment.END,
      wrap=True,
      controls=[
          make_stat_card(
              "حالات الفيض", card_surplus, ft.Icons.ADD_ALERT, "orange"
          ),
          make_stat_card("حالات الشاغر", card_vacant, ft.Icons.WARNING, "red"),
          make_stat_card("إجمالي المدارس", card_total, ft.Icons.SCHOOL, "blue"),
      ],
  )

  footer_section = ft.Row(
      alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      controls=[
          ft.Text(
              "تصميم وتطوير: ضرغام مهدي صلال",
              size=12,
              color="grey",
              weight=ft.FontWeight.BOLD,
          ),
          ft.Text("نظام الإشراف التربوي © 2026", size=12, color="grey"),
      ],
  )

  main_layout = ft.Container(
      expand=True,
      gradient=ft.LinearGradient(
          begin=ft.Alignment(-1, -1),
          end=ft.Alignment(1, 1),
          colors=["#eef2f3", "#8e9eab"],
      ),
      padding=25,
      content=ft.Column(
          scroll=ft.ScrollMode.AUTO,
          alignment=ft.MainAxisAlignment.START,
          horizontal_alignment=ft.CrossAxisAlignment.END,
          controls=[
              ft.Row(
                  alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                  controls=[
                      btn_export,
                      ft.Text(
                          "نظام الإشراف التربوي - إدارات المدارس",
                          size=24,
                          weight=ft.FontWeight.BOLD,
                          color="#1e293b",
                      ),
                  ],
              ),
              ft.Divider(height=15, color="transparent"),
              stats_row,
              ft.Divider(height=15, color="transparent"),
              ft.Card(
                  elevation=3,
                  content=ft.Container(
                      padding=20,
                      border_radius=10,
                      content=ft.Column(
                          horizontal_alignment=ft.CrossAxisAlignment.END,
                          controls=[
                              ft.Row(
                                  [txt_spec, txt_school],
                                  alignment=ft.MainAxisAlignment.END,
                                  wrap=True,
                              ),
                              ft.Row(
                                  [btn_cancel, btn_add, txt_curr, txt_req],
                                  alignment=ft.MainAxisAlignment.END,
                                  wrap=True,
                              ),
                              status_label,
                          ],
                      ),
                  ),
              ),
              ft.Divider(height=15, color="transparent"),
              ft.Card(
                  elevation=3,
                  content=ft.Container(
                      padding=20,
                      border_radius=10,
                      content=ft.Column(
                          horizontal_alignment=ft.CrossAxisAlignment.END,
                          controls=[
                              ft.Row(
                                  [
                                      ft.Row(
                                          [txt_search_school, filter_dropdown],
                                          wrap=True,
                                          alignment=ft.MainAxisAlignment.END,
                                      ),
                                      ft.Text(
                                          "جدول المدارس المحفوظة",
                                          size=18,
                                          weight=ft.FontWeight.BOLD,
                                          color="#334155",
                                      ),
                                  ],
                                  alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                  wrap=True,
                              ),
                              ft.Divider(height=10, color="transparent"),
                              ft.Row(
                                  [data_table],
                                  alignment=ft.MainAxisAlignment.END,
                                  scroll=ft.ScrollMode.ALWAYS,
                              ),
                          ],
                      ),
                  ),
              ),
              ft.Divider(height=15, color="transparent"),
              footer_section,
          ],
      ),
  )

  page.add(main_layout)
  refresh_table()


ft.run(main)
